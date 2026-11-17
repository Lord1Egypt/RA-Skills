#!/usr/bin/env bash
# Maestro mobile testing setup script
# Installs Java 17, Maestro CLI, and verifies the Android SDK + emulator.
#
# Usage:
#   bash skills/maestro-mobile-test/scripts/setup.sh
#
# Works on: macOS, Linux, Windows (git-bash / MSYS2)
#
# Prerequisites (not installed by this script):
#   - Android SDK (Android Studio)
#   - At least one AVD (emulator image) — create via Android Studio AVD Manager

set -euo pipefail

echo "=== Maestro mobile testing setup ==="
echo "Platform: $(uname -s)"
echo ""

# --- Detect platform ---
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) IS_WINDOWS=1 ;;
  Darwin)               IS_WINDOWS=0 ;;
  Linux)
    # Check for WSL (reports as Linux but needs different JDK paths)
    if grep -qi "microsoft\|WSL" /proc/version 2>/dev/null; then
      IS_WINDOWS=0  # WSL uses Linux JDKs, but Windows SDK via /mnt/c
    else
      IS_WINDOWS=0
    fi
    ;;
  *)                    IS_WINDOWS=0 ;;
esac

# --- Check Android SDK ---
echo "--- Android SDK ---"
if [ -z "${ANDROID_HOME:-}" ]; then
    # Try platform-standard locations (including WSL's /mnt/c mount)
    for sdk_path in \
        "$HOME/AppData/Local/Android/Sdk" \
        "$HOME/Library/Android/sdk" \
        "/usr/local/share/android-sdk" \
        "/opt/android-sdk" \
        "/mnt/c/Users/$USER/AppData/Local/Android/Sdk"; do
        if [ -d "$sdk_path" ]; then
            export ANDROID_HOME="$sdk_path"
            break
        fi
    done
fi

if [ -z "${ANDROID_HOME:-}" ]; then
    echo "❌ ANDROID_HOME not set and SDK not found in standard locations."
    echo "   Install Android Studio or set ANDROID_HOME manually."
    echo "   Standard locations checked:"
    echo "     Windows: ~/AppData/Local/Android/Sdk"
    echo "     macOS:   ~/Library/Android/sdk"
    echo "     Linux:   /opt/android-sdk"
    exit 1
fi
echo "ANDROID_HOME: $ANDROID_HOME"

if [ ! -d "$ANDROID_HOME/emulator" ] || [ ! -d "$ANDROID_HOME/platform-tools" ]; then
    echo "❌ Android SDK incomplete — missing emulator or platform-tools."
    exit 1
fi
echo "✅ Android SDK found"

export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$PATH"

# --- Check for AVDs ---
echo ""
echo "--- Emulator images ---"
EMULATOR_BIN="emulator"
[ "$IS_WINDOWS" = "1" ] && EMULATOR_BIN="emulator.exe"
AVDS=$("$ANDROID_HOME/emulator/$EMULATOR_BIN" -list-avds 2>/dev/null || true)

if [ -z "$AVDS" ]; then
    echo "❌ No AVDs found. Create one via Android Studio → AVD Manager."
    exit 1
fi
echo "Available AVDs:"
echo "$AVDS" | sed 's/^/  /'
echo "✅ AVDs present"

# --- Check / install Java 17 ---
echo ""
echo "--- Java ---"
INSTALL_JAVA=0
if command -v java &>/dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -1 | grep -oE '[0-9]+' | head -1)
    if [ "$JAVA_VERSION" -ge 17 ] 2>/dev/null; then
        echo "✅ Java $JAVA_VERSION found"
    else
        echo "⚠️  Java found but version $JAVA_VERSION < 17. Installing JDK 17..."
        INSTALL_JAVA=1
    fi
else
    echo "Java not found. Installing JDK 17..."
    INSTALL_JAVA=1
fi

if [ "$INSTALL_JAVA" = "1" ]; then
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*)
        echo "Installing Microsoft OpenJDK 17..."
        powershell.exe -NoProfile -Command "winget install --id Microsoft.OpenJDK.17 --accept-package-agreements --accept-source-agreements" 2>&1 || {
            echo "⚠️  winget install may need admin approval. If it failed, install JDK 17 manually:"
            echo "   https://learn.microsoft.com/java/openjdk/"
        }
        # Detect the installed JDK path
        for jdk in "/c/Program Files/Microsoft/jdk-17"*; do
            if [ -d "$jdk" ]; then
                export JAVA_HOME="$jdk"
                break
            fi
        done
        ;;
      Darwin)
        if command -v brew &>/dev/null; then
            brew install --cask temurin@17
            export JAVA_HOME="$(/usr/libexec/java_home -v 17 2>/dev/null || true)"
        else
            echo "❌ Homebrew not found. Install JDK 17 manually: https://adoptium.net/"
            exit 1
        fi
        ;;
      Linux)
        if command -v apt-get &>/dev/null; then
            sudo apt-get update && sudo apt-get install -y openjdk-17-jdk
            export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y java-17-openjdk-devel
            export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
        else
            echo "❌ No supported package manager. Install JDK 17 manually: https://adoptium.net/"
            exit 1
        fi
        ;;
    esac
fi

# --- Check / install Maestro ---
echo ""
echo "--- Maestro CLI ---"
if command -v maestro &>/dev/null; then
    MAESTRO_VERSION=$(maestro --version 2>&1 | head -1)
    echo "✅ Maestro found: $MAESTRO_VERSION"
else
    echo "Installing Maestro CLI..."
    if [ -n "${JAVA_HOME:-}" ]; then
        export PATH="$JAVA_HOME/bin:$PATH"
    fi
    curl -Ls "https://get.maestro.mobile.dev" | bash
    echo ""
    export PATH="$HOME/.maestro/bin:$PATH"
    echo "✅ Maestro installed to ~/.maestro/bin"
fi

# --- Write env helper ---
echo ""
echo "--- Writing environment helper ---"
ENV_HELPER="$HOME/.maestro/activate.sh"
cat > "$ENV_HELPER" << 'EOF'
#!/usr/bin/env bash
# Maestro environment setup — source before running tests.
# Usage: source ~/.maestro/activate.sh
# Guard: fail clearly if executed instead of sourced
(return 0 2>/dev/null) || { echo "❌ Source this file: source ~/.maestro/activate.sh"; exit 1; }

# Detect ANDROID_HOME at activation time (don't hardcode the setup-time path)
if [ -z "${ANDROID_HOME:-}" ]; then
    for _sdk in \
        "$HOME/Library/Android/sdk" \
        "$HOME/AppData/Local/Android/Sdk" \
        "/usr/local/share/android-sdk" \
        "/opt/android-sdk"; do
        if [ -d "$_sdk" ]; then
            export ANDROID_HOME="$_sdk"
            break
        fi
    done
fi
export ANDROID_SDK_ROOT="${ANDROID_HOME}"

# Detect JAVA_HOME at activation time
if [ -z "${JAVA_HOME:-}" ]; then
    # Auto-detect via java binary location
    if command -v java &>/dev/null; then
        JAVA_PATH=$(readlink -f $(which java) 2>/dev/null || realpath $(which java) 2>/dev/null || echo "")
        if [ -n "$JAVA_PATH" ]; then
            export JAVA_HOME=$(dirname $(dirname "$JAVA_PATH"))
        fi
    fi
    # macOS specific
    if [ "$(uname -s)" = "Darwin" ] && [ -z "${JAVA_HOME:-}" ]; then
        export JAVA_HOME="$(/usr/libexec/java_home 2>/dev/null || true)"
    fi
    # Windows JDK locations
    for _jdk in "/c/Program Files/Microsoft/jdk-17"* "/c/Program Files/Eclipse Adoptium/jdk-17"*; do
        if [ -d "$_jdk" ] && [ -z "${JAVA_HOME:-}" ]; then
            export JAVA_HOME="$_jdk"
            break
        fi
    done
fi

export PATH="${JAVA_HOME}/bin:${HOME}/.maestro/bin:${ANDROID_HOME}/emulator:${ANDROID_HOME}/platform-tools:${PATH}"

echo "✅ Maestro environment ready"
echo "   JAVA_HOME:    ${JAVA_HOME:-not detected}"
echo "   ANDROID_HOME: ${ANDROID_HOME:-not detected}"
EOF
chmod +x "$ENV_HELPER"
echo "Wrote: $ENV_HELPER"

# --- Summary ---
echo ""
echo "=== Setup complete ==="
echo ""
echo "Environment variables:"
echo "  ANDROID_HOME: $ANDROID_HOME"
echo "  JAVA_HOME:    ${JAVA_HOME:-<detect at runtime>}"
echo ""
echo "To activate:"
echo "  source ~/.maestro/activate.sh"
echo ""
echo "To boot an emulator and run a test:"
echo "  bash skills/maestro-mobile-test/scripts/run_flow.sh <avd-name> .maestro/navigation/tab-nav.yaml"
