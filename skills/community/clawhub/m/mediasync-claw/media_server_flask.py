#!/usr/bin/env python3
"""
OpenClaw Skill: Media File Server with FRP + WebRTC P2P Support

Architecture:
  - Flask serves HTTP routes (API, media files, player page)
  - Flask-SocketIO handles WebSocket signaling (same port as Flask)
  - aiortc handles WebRTC P2P data channels for media streaming
  - An asyncio event loop runs in a background thread for aiortc operations
  - FRP tunnels all traffic (signaling + media fallback) through FRPS
  - WebRTC P2P bypasses FRPS for actual media data, saving bandwidth
"""

import os
import json
import hashlib
import asyncio
import threading
from urllib.parse import quote

from flask import Flask, render_template, abort, jsonify, send_file, Response
from flask import request
from flask_socketio import SocketIO
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel, RTCIceCandidate
from aiortc.exceptions import InvalidStateError
from aiortc.sdp import candidate_from_sdp
import concurrent.futures
import aiofiles

from media_frp_util import get_domain, setup_frp
from media_file_util import get_media_directory, get_media_files

# ── Initialize Flask + SocketIO (same port, no extra FRP proxy needed) ──
app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# ── Global state for WebRTC ──
async_loop = None          # asyncio event loop running in a background thread
loop_ready = threading.Event()  # signals when async_loop is initialized
peer_connections = {}      # sid -> RTCPeerConnection
pc_lock = threading.Lock()  # protects peer_connections dict

def generate_md5_checksum(s: str) -> str:
    encoded_data = s.encode('utf-8')
    return hashlib.md5(encoded_data).hexdigest()

# ══════════════════════════════════════════════════════════════
#  Flask HTTP Routes
# ══════════════════════════════════════════════════════════════

@app.route('/api/list_files', methods=['POST'])
def handle_api_list_files():
    """WhatsApp API endpoint — returns a playlist of WebRTC player URLs."""
    try:
        frp_domain = get_domain()
        print(f"DEBUG: frp_domain = {frp_domain}")

        # Use plain text instead of emoji to avoid encoding issues on Windows
        txt = "*The file below is a playlist of all available media files:*\n\n"
        media_files = get_media_files()
        print(f"DEBUG: media_files = {media_files}")
        if isinstance(media_files, list) and len(media_files) > 0:
            for media_file in media_files:
                media_file_name = os.path.basename(media_file)
                # WebRTC player URL — browser opens this to start P2P streaming
                media_file_url = f"http://{frp_domain}/{media_file_name}"
                media_file_url_with_query = "videourl=" + media_file_url
                media_file_url_with_cs = f"&cks={generate_md5_checksum(media_file_url_with_query)}"
                aiplayer_url = f"https://yun-hub.chat/link/?app=aipollo&clickid=12345&dplink={quote(media_file_url_with_query + media_file_url_with_cs, safe='')}"
                txt += f"{media_file_name}: {aiplayer_url}\n"
        else:
            txt += "No media files found."
        return jsonify({"text": txt}), 200
    except Exception as e:
        print(f"ERROR in handle_api_list_files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/play')
def serve_player():
    """Serves the WebRTC player HTML page."""
    filename = request.args.get('file')
    if not filename:
        abort(400)
    return render_template('player.html', filename=filename)

# ══════════════════════════════════════════════════════════════
#  WebRTC Signaling (Flask-SocketIO WebSocket handlers)
# ══════════════════════════════════════════════════════════════

@socketio.on('connect')
def handle_connect():
    """Create a new RTCPeerConnection for each connected client."""
    from aiortc import RTCConfiguration, RTCIceServer
    sid = request.sid
    
    # ICE servers: STUN for NAT traversal, TURN as fallback for symmetric NATs
    configuration = RTCConfiguration(iceServers=[
        # Google
        RTCIceServer(urls="stun:stun.l.google.com:19302"),
        RTCIceServer(urls="stun:stun1.l.google.com:19302"),
        # Cloudflare
        RTCIceServer(urls="stun:stun.cloudflare.com:3478"),
        # Twilio 
        RTCIceServer(urls="stun:global.stun.twilio.com:3478")
    ])
    pc = RTCPeerConnection(configuration)
    with pc_lock:
        peer_connections[sid] = pc
    print(f"[WebRTC] Client connected: {sid} (active sessions: {len(peer_connections)})")

    # ── Fix #1: Relay ICE candidates from server (aiortc) → browser ──
    @pc.on("icecandidate")
    async def on_ice_candidate(candidate):
        if candidate:
            socketio.emit('ice_candidate', {
                'candidate': str(candidate),
                'sdpMid': candidate.sdpMid,
                'sdpMLineIndex': candidate.sdpMLineIndex
            }, room=sid)

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"[WebRTC] DataChannel opened for {sid}")

        @channel.on("message")
        def on_message(message):
            # Handle text commands (e.g. "request:video.mp4")
            if isinstance(message, str) and message.startswith("request:"):
                filename = os.path.basename(message.split(":", 1)[1])
                media_dir = os.path.realpath(get_media_directory())
                filepath = os.path.realpath(os.path.join(media_dir, filename))

                if not filename or not filepath.startswith(media_dir + os.sep):
                    channel.send(json.dumps({"error": "forbidden"}))
                    return

                if not os.path.isfile(filepath):
                    channel.send(json.dumps({"error": "file not found"}))
                    return

                file_size = os.path.getsize(filepath)
                channel.send(json.dumps({
                    "type": "meta",
                    "size": file_size,
                    "name": filename,
                }))

                # ── Fix #3: Stream file entirely within the asyncio event loop ──
                async def stream_file_async():
                    try:
                        async with aiofiles.open(filepath, "rb") as f:
                            BUFFER_THRESHOLD = 1 * 1024 * 1024 
                            chunk_size = 16 * 1024
                            consecutive_full_buffer = 0
                            max_consecutive_full = 100  # ~2.5 seconds at 50ms intervals
                            
                            while True:
                                # Check both DataChannel and PeerConnection state
                                if channel.readyState != 'open' or pc.connectionState in ('closed', 'failed', 'disconnected'):
                                    print(f"[WebRTC] Connection dead for {sid}, channel: {channel.readyState}, pc: {pc.connectionState}")
                                    return

                                chunk = await f.read(chunk_size)
                                if not chunk:
                                    break
                                
                                # Backpressure: yield to event loop if buffer is full
                                while getattr(channel, 'bufferedAmount', 0) > BUFFER_THRESHOLD:
                                    buffered = getattr(channel, 'bufferedAmount', 0)
                                    print(f"[WebRTC] bufferAmount overflow: {buffered / 1024:.0f}KB for {sid}, channel: {channel.readyState}, pc: {pc.connectionState}")
                                    
                                    # Channel is closing/closed - buffer will never drain
                                    if channel.readyState != 'open' or pc.connectionState in ('closed', 'failed', 'disconnected'):
                                        print(f"[WebRTC] Connection lost during backpressure for {sid}")
                                        return
                                    
                                    # Detect stuck buffer: if buffer stays high for too long, channel is likely dead
                                    consecutive_full_buffer += 1
                                    if consecutive_full_buffer > max_consecutive_full:
                                        print(f"[WebRTC] Buffer stuck for {max_consecutive_full * 100}ms, assuming channel dead for {sid}")
                                        return
                                    
                                    await asyncio.sleep(0.1)
                                
                                # Reset counter when buffer is healthy
                                consecutive_full_buffer = 0
                                
                                try:
                                    channel.send(chunk)
                                except InvalidStateError:
                                    print(f"[WebRTC] Channel closed during send for {sid}")
                                    return

                                buffered = getattr(channel, 'bufferedAmount', 0)
                                if buffered > BUFFER_THRESHOLD * 0.7:
                                    await asyncio.sleep(0.08)
                                elif buffered > BUFFER_THRESHOLD * 0.3:
                                    await asyncio.sleep(0.01)
                                else:
                                    await asyncio.sleep(0.005)
                        
                        # Only send "done" if channel is still open
                        if channel.readyState == 'open' and pc.connectionState not in ('closed', 'failed', 'disconnected'):
                            channel.send(json.dumps({"type": "done"}))
                        print(f"[WebRTC] File streaming completed for {sid}")
                        
                    except InvalidStateError:
                        print(f"[WebRTC] Channel closed during streaming for {sid}")
                    except Exception as e:
                        print(f"[WebRTC] Unexpected error streaming file for {sid}: {e}")

                future = asyncio.run_coroutine_threadsafe(stream_file_async(), async_loop)
                future.add_done_callback(
                    lambda f: f.exception() and print(f"[WebRTC] Stream error: {f.exception()}")
                )

    @pc.on("connectionstatechange")
    def on_connection_state():
        state = pc.connectionState
        print(f"[WebRTC] Connection state for {sid}: {state}")
        if state in ("closed", "failed"):
            with pc_lock:
                is_current_pc = peer_connections.get(sid) is pc
                if is_current_pc:
                    peer_connections.pop(sid, None)

            if is_current_pc:
                try:
                    asyncio.run_coroutine_threadsafe(pc.close(), async_loop)
                except Exception as e:
                    print(f"[WebRTC] Error closing PeerConnection for {sid}: {e}")
            print(f"[WebRTC] PeerConnection closed for {sid}")

@socketio.on('offer')
def handle_offer(data):
    """Handle SDP offer from the browser and respond with an SDP answer."""
    sid = request.sid
    with pc_lock:
        pc = peer_connections.get(sid)
    if not pc:
        return

    async def process():
        try:
            await pc.setRemoteDescription(
                RTCSessionDescription(sdp=data['sdp'], type="offer"))
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            socketio.emit('answer', {'sdp': pc.localDescription.sdp}, room=sid)
        except Exception as e:
            print(f"[WebRTC] Offer processing exception for {sid}: {e}")
            with pc_lock:
                if peer_connections.get(sid) is pc:
                    peer_connections.pop(sid, None)
            await pc.close()
            
    future = asyncio.run_coroutine_threadsafe(process(), async_loop)

    def handle_future_exception(fut):
        try:
            fut.result()
        except Exception as e:
            print(f"[WebRTC] Unexpected error in offer future for {sid}: {e}")
    future.add_done_callback(handle_future_exception)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Forward ICE candidates from the browser to the local peer."""
    sid = request.sid
    with pc_lock:
        pc = peer_connections.get(sid)
    if not pc:
        return

    candidate_str = data.get('candidate')
    if candidate_str:
        async def add_candidate():
            try:
                candidate_obj = candidate_from_sdp(candidate_str)
                candidate_obj.sdpMid = data.get('sdpMid')
                candidate_obj.sdpMLineIndex = data.get('sdpMLineIndex')
                await pc.addIceCandidate(candidate_obj)
            except Exception as e:
                print(f"[WebRTC] Error adding ICE candidate for {sid}: {e}")
        asyncio.run_coroutine_threadsafe(add_candidate(), async_loop)


@socketio.on('disconnect')
def handle_disconnect():
    """Clean up the peer connection when a client disconnects."""
    sid = request.sid
    with pc_lock:
        pc = peer_connections.pop(sid, None)
    if pc:
        async def close_pc():
            try:
                # Ensure all data channels are closed first
                for t in pc.getTransceivers():
                    try:
                        if t.mid is not None:
                            t.stop()
                    except Exception:
                        pass
                
                await pc.close()
            except Exception as e:
                print(f"[WebRTC] Error closing PeerConnection for {sid}: {e}")
            
        future = asyncio.run_coroutine_threadsafe(close_pc(), async_loop)
        
        try:
            success = future.result(timeout=5.0)
            print(f"[WebRTC] Synchronous cleanup finished for {sid}. Success: {success}")
        except concurrent.futures.TimeoutError:
            print(f"[WebRTC] WARNING: pc.close() timed out for {sid}! Async loop might be congested.")
        except Exception as e:
            print(f"[WebRTC] Future result exception for {sid}: {e}")
            
    print(f"[WebRTC] Client disconnect callback completely finished: {sid}")

# ══════════════════════════════════════════════════════════════
#  Asyncio Bridge — runs aiortc's event loop in a background thread
# ══════════════════════════════════════════════════════════════

def async_exception_handler(loop, context):
    """Custom exception handler for the asyncio event loop.

    aiortc's internal tasks can raise exceptions that are never awaited,
    causing Python to print 'Task exception was never retrieved' warnings.
    Known benign cases:
      - ConnectionError from RTCSctpTransport._transmit (ICE dropped)
      - InvalidStateError from RTCPeerConnection.__connect (ICE closed)
    We suppress these and only forward truly unexpected errors.
    """
    exception = context.get('exception')
    message = context.get('message', '')

    # Suppress known benign aiortc warnings
    if isinstance(exception, (ConnectionError, InvalidStateError)):
        return

    if 'Task exception was never retrieved' in message:
        if isinstance(exception, (ConnectionError, InvalidStateError)):
            return
        # Don't print these during normal operation
        return

    # Suppress "Task was destroyed but it is pending!" warnings from aiortc internals
    if 'Task was destroyed but it is pending' in message:
        return

    loop.default_exception_handler(context)


def start_async_loop():
    """Start a dedicated asyncio event loop in a daemon thread for aiortc."""
    global async_loop
    async_loop = asyncio.new_event_loop()
    async_loop.set_exception_handler(async_exception_handler)
    asyncio.set_event_loop(async_loop)
    loop_ready.set()

    try:
        async_loop.run_forever()
    finally:
        try:
            # Give aiortc's internal tasks time to clean up gracefully
            pending = asyncio.all_tasks(async_loop)
            if pending:
                print(f"[Async] Cancelling {len(pending)} pending tasks...")
                for task in pending:
                    task.cancel()

                # Allow tasks to handle cancellation properly
                async_loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )
                
                # Second pass: cancel any tasks that spawned during cleanup
                remaining = asyncio.all_tasks(async_loop)
                if remaining:
                    for task in remaining:
                        task.cancel()
                    async_loop.run_until_complete(
                        asyncio.gather(*remaining, return_exceptions=True)
                    )
        except Exception as e:
            print(f"[Async] Error while canceling pending tasks: {e}")
        finally:
            async_loop.close()
            print("[Async] Event loop closed gracefully.")


# ══════════════════════════════════════════════════════════════
#  Server Startup
# ══════════════════════════════════════════════════════════════

def setup_media_server(port=8000):
    """Start the Flask + SocketIO media server."""
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    os.chdir(current_directory)

    print("Press Ctrl+C to stop the server")

    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=False,
        allow_unsafe_werkzeug=True,
    )


def main():
    # Shared stop event to signal FRP thread to exit
    stop_event = threading.Event()

    # 1. Start the asyncio event loop for aiortc (background thread)
    threading.Thread(target=start_async_loop, daemon=True).start()

    loop_ready.wait()

    # 2. Setup FRP tunnel (HTTPS via FRPS)
    setup_frp(port=8000, stop_event=stop_event)

    # 3. Start the Flask + SocketIO media server (blocks main thread)
    try:
        setup_media_server(port=8000)
    finally:
        print("\nShutting down FRP tunnel...")
        stop_event.set()


if __name__ == '__main__':
    main()