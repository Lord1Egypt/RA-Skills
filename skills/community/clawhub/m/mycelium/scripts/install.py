import subprocess
import sys

def install_deps():
    print("Checking Mycelium dependencies...")
    try:
        import httpx
        print("✅ httpx already installed.")
    except ImportError:
        print("Installing httpx...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx"])
    print("Done.")

if __name__ == "__main__":
    install_deps()
