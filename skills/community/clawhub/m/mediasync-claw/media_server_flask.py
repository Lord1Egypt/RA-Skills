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
import asyncio
import threading
from urllib.parse import quote_plus

from flask import Flask, render_template, abort, jsonify, request
from flask_socketio import SocketIO
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

from media_frp_util import get_domain, setup_frp
from media_file_util import get_media_directory, get_media_files

# ── Initialize Flask + SocketIO (same port, no extra FRP proxy needed) ──
app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Global state for WebRTC ──
async_loop = None          # asyncio event loop running in a background thread
peer_connections = {}      # sid -> RTCPeerConnection


# ══════════════════════════════════════════════════════════════
#  Flask HTTP Routes
# ══════════════════════════════════════════════════════════════

@app.route('/api/openclaw', methods=['POST'])
def handle_api_openclaw():
    """WhatsApp API endpoint — returns a playlist of WebRTC player URLs."""
    frp_domain = get_domain()

    txt = "🎬 *The file below is a playlist of all available media files:*\n\n"
    media_files = get_media_files()
    if isinstance(media_files, list) and len(media_files) > 0:
        for media_file in media_files:
            media_file_name = os.path.basename(media_file)
            # WebRTC player URL — browser opens this to start P2P streaming
            media_file_url = f"http://{frp_domain}/{media_file_name}"
            player_url = f"https://yun-hub.chat/link/?app=aipollo&clickid=12345&videourl={quote_plus(media_file_url)}"
            txt += f"{media_file_name}: {player_url}\n"
    else:
        txt += "No media files found."
    return jsonify({"text": txt}), 200

# @app.route('/play')
# def serve_player():
#     """Serves the WebRTC player HTML page."""
#     filename = request.args.get('file')
#     if not filename:
#         abort(400)
#     return render_template('player.html', filename=filename)


# ══════════════════════════════════════════════════════════════
#  WebRTC Signaling (Flask-SocketIO WebSocket handlers)
# ══════════════════════════════════════════════════════════════

@socketio.on('connect')
def handle_connect():
    """Create a new RTCPeerConnection for each connected client."""
    from flask import request as flask_request
    from aiortc import RTCConfiguration, RTCIceServer
    sid = flask_request.sid
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
    peer_connections[sid] = pc
    print(f"[WebRTC] Client connected: {sid}")

    # ── Fix #1: Relay ICE candidates from server (aiortc) → browser ──
    @pc.on("icecandidate")
    async def on_ice_candidate(candidate):
        if candidate:
            socketio.emit('ice_candidate', {'candidate': candidate}, room=sid)

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"[WebRTC] DataChannel opened for {sid}")

        @channel.on("message")
        def on_message(message):
            # Handle text commands (e.g. "request:video.mp4")
            if isinstance(message, str) and message.startswith("request:"):
                filename = message.split(":", 1)[1]
                filepath = os.path.join(get_media_directory(), filename)

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
                        with open(filepath, "rb") as f:
                            while True:
                                chunk = f.read(65536)
                                if not chunk:
                                    break
                                # Backpressure: yield to event loop if buffer is full
                                while channel.bufferedAmount > 16 * 1024 * 1024:
                                    await asyncio.sleep(0.05)
                                channel.send(chunk)
                        channel.send(json.dumps({"type": "done"}))
                    except Exception as e:
                        print(f"[WebRTC] Streaming error: {e}")

                asyncio.run_coroutine_threadsafe(stream_file_async(), async_loop)

    @pc.on("connectionstatechange")
    def on_connection_state():
        state = pc.connectionState
        print(f"[WebRTC] Connection state for {sid}: {state}")
        if state in ("closed", "failed"):
            peer_connections.pop(sid, None)


@socketio.on('offer')
def handle_offer(data):
    """Handle SDP offer from the browser and respond with an SDP answer."""
    from flask import request as flask_request
    sid = flask_request.sid
    pc = peer_connections.get(sid)
    if not pc:
        return

    async def process():
        await pc.setRemoteDescription(
            RTCSessionDescription(sdp=data['sdp'], type="offer")
        )
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return pc.localDescription.sdp

    future = asyncio.run_coroutine_threadsafe(process(), async_loop)
    answer_sdp = future.result()
    socketio.emit('answer', {'sdp': answer_sdp}, room=sid)


@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Forward ICE candidates from the browser to the local peer."""
    from flask import request as flask_request
    sid = flask_request.sid
    pc = peer_connections.get(sid)
    if not pc:
        return

    candidate = data.get('candidate')
    if candidate:
        async def add_candidate():
            await pc.addIceCandidate(candidate)
        asyncio.run_coroutine_threadsafe(add_candidate(), async_loop)


@socketio.on('disconnect')
def handle_disconnect():
    """Clean up the peer connection when a client disconnects."""
    from flask import request as flask_request
    sid = flask_request.sid
    pc = peer_connections.pop(sid, None)
    if pc:
        async def close_pc():
            await pc.close()
        asyncio.run_coroutine_threadsafe(close_pc(), async_loop)
    print(f"[WebRTC] Client disconnected: {sid}")


# ══════════════════════════════════════════════════════════════
#  Asyncio Bridge — runs aiortc's event loop in a background thread
# ══════════════════════════════════════════════════════════════

def start_async_loop():
    """Start a dedicated asyncio event loop in a daemon thread for aiortc."""
    global async_loop
    async_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(async_loop)
    async_loop.run_forever()


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