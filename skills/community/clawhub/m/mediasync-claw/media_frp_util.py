import os
import subprocess
import hashlib
import time
import requests
import zipfile
import io
from uuid_config import UUIDConfig

# ── Pinned SHA256 checksums for frp v0.65.0 (frpc.exe inside the zip) ──
# These must be updated when the FRP version is bumped.
# Source: https://github.com/fatedier/frp/releases/tag/v0.65.0
FRP_VERSION = "0.65.0"
FRP_ZIP_SHA256 = "5885bff09604e719e429698f800f89379f3910f074990ca1f7d8a7f7a40970eda"
FRPC_EXE_SHA256 = "5b0846d4a5e9bcde0960b354fd819eb0011529ff23f41ad55a8717ba5c7004ac"


def get_domain():
    uuid_config_instance = UUIDConfig()
    uuid_value = uuid_config_instance.get_uuid()
    return uuid_value + ".yunfrp.net"


def download_frp():
    """Download frpc.exe from GitHub Releases with SHA256 integrity verification.

    Returns:
        True if frpc.exe already exists or was downloaded and verified successfully.
        False if download or verification fails.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    frpc_path = os.path.join(current_directory, "frpc.exe")

    # If already present, skip download (existing binary is trusted once verified)
    if os.path.exists(frpc_path):
        return True

    frp_url = f"https://github.com/fatedier/frp/releases/download/v{FRP_VERSION}/frp_{FRP_VERSION}_windows_amd64.zip"

    try:
        print(f"[FRP] Downloading frpc.exe v{FRP_VERSION} from GitHub...")
        r = requests.get(frp_url, timeout=60)
        r.raise_for_status()

        zip_data = r.content

        # ── Layer 1: Verify the zip archive checksum before extraction ──
        zip_hash = hashlib.sha256(zip_data).hexdigest()
        if zip_hash != FRP_ZIP_SHA256:
            print(f"[FRP] SECURITY ERROR: Zip checksum mismatch!")
            print(f"  Expected: {FRP_ZIP_SHA256}")
            print(f"  Got:      {zip_hash}")
            print(f"  The download may have been tampered with or corrupted. Aborting.")
            return False
        print(f"[FRP] Zip SHA256 verified: {zip_hash[:16]}...")

        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
            frpc_member = None
            for member in zf.namelist():
                if member.endswith("frpc.exe"):
                    frpc_member = member
                    break

            if not frpc_member:
                print("[FRP] ERROR: frpc.exe not found in the downloaded archive.")
                return False

            exe_data = zf.read(frpc_member)

            # ── Layer 2: Verify frpc.exe checksum after extraction ──
            exe_hash = hashlib.sha256(exe_data).hexdigest()
            if exe_hash != FRPC_EXE_SHA256:
                print(f"[FRP] SECURITY ERROR: frpc.exe checksum mismatch!")
                print(f"  Expected: {FRPC_EXE_SHA256}")
                print(f"  Got:      {exe_hash}")
                print(f"  Aborting.")
                return False
            print(f"[FRP] frpc.exe SHA256 verified: {exe_hash[:16]}...")

            # Extract and place in the script directory
            zf.extract(frpc_member, current_directory)
            extracted = os.path.join(current_directory, frpc_member)
            if extracted != frpc_path:
                os.rename(extracted, frpc_path)

        print(f"[FRP] frpc.exe v{FRP_VERSION} downloaded and verified successfully.")
        return True

    except requests.RequestException as e:
        print(f"[FRP] Network error downloading frpc: {e}")
        return False
    except Exception as e:
        print(f"[FRP] Unexpected error: {e}")
        return False


def setup_frp_and_keep_alive(port=8000, frp_config=None, stop_event=None):
    """
    Setup FRP tunnel for remote access to the media server.
    Flask + SocketIO (HTTP + WebSocket signaling) both run on the same port,
    so only one FRP proxy entry is needed.

    Args:
        port (int): Local port where Flask media server is running
        frp_config (str): Path to FRP configuration file
        stop_event (threading.Event): Signal to stop the keep-alive loop
    """
    print(f"DEBUG: setup_frp called with local_port={port}, frp_config={frp_config}")

    if frp_config is None:
        frp_domain = get_domain()
        frp_config_content = f'''
            serverAddr = "129.213.174.213"
            serverPort = 7000

            webServer.addr = "127.0.0.1"
            webServer.port = 7400

            [transport]
            heartbeatInterval = 30
            heartbeatTimeout = 90
            tcpMux = true
            tcpMuxKeepaliveInterval = 30

            [[proxies]]
            name = "{frp_domain}"
            type = "http"
            customDomains = ["{frp_domain}"]
            localPort = {port}
        '''
        frp_config = "frpc.toml"
        with open(frp_config, 'w') as f:
            f.write(frp_config_content.strip())

        print(f"Started FRP tunnel using config: {frp_config_content}")

    # Validate frp_config: only allow config files within the script directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    resolved_config = os.path.realpath(os.path.join(current_directory, frp_config))
    if not resolved_config.startswith(os.path.realpath(current_directory) + os.sep):
        raise ValueError(f"FRP config path outside allowed directory: {frp_config}")

    frp_process = None
    try:
        frpc_path = os.path.join(current_directory, "frpc.exe")
        if not os.path.isfile(frpc_path):
            raise FileNotFoundError(f"FRP client not found: {frpc_path}")
        if not os.path.isfile(resolved_config):
            raise FileNotFoundError(f"FRP config not found: {resolved_config}")

        frp_process = subprocess.Popen(
            [frpc_path, '-c', resolved_config],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        while not (stop_event and stop_event.is_set()):
            poll_result = frp_process.poll()

            if poll_result is not None:
                if stop_event and stop_event.is_set():
                    break
                frp_process = subprocess.Popen(
                    [frpc_path, '-c', resolved_config],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False)
                continue

            time.sleep(1)
    except Exception:
        print(f"Error: FRP client not found at {frpc_path}.")
        print("Please ensure frpc.exe is in the media-file-server directory")
    finally:
        if frp_process and frp_process.poll() is None:
            frp_process.terminate()
            try:
                frp_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frp_process.kill()
            print("[FRP] frpc stopped.")


def setup_frp(port=8000, stop_event=None):
    """Download FRP client if needed, then start the FRP tunnel in a background thread."""
    if not download_frp():
        print("Error: Failed to download frpc.exe")
        return

    import threading
    frp_thread = threading.Thread(target=setup_frp_and_keep_alive, args=(port, None, stop_event), daemon=False)
    frp_thread.start()