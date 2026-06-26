#!/usr/bin/env bash
set -euo pipefail

# ─── Paths ────────────────────────────────────────────────────────────────────
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${SKILL_DIR}/.skill-config"

# ─── Defaults ─────────────────────────────────────────────────────────────────
NAME=""
MODE="static"
IDEA=""
WORKDIR="${PWD}"
SKIP_DEPLOY="false"
RUN_SETUP="false"

usage() {
  echo "Usage: $0 [--setup] [--name <app-name>] [--mode static|nextjs] [--idea <text>] [--workdir <path>] [--skip-deploy]"
  echo ""
  echo "  --setup        Re-run the interactive onboarding wizard"
  echo "  --name         App folder name (required unless --setup)"
  echo "  --mode         static (default) or nextjs"
  echo "  --idea         One-liner describing the app (optional)"
  echo "  --workdir      Parent directory for the app folder (default: cwd)"
  echo "  --skip-deploy  Scaffold only, no Vercel deploy"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --setup)      RUN_SETUP="true"; shift 1 ;;
    --name)       NAME="$2"; shift 2 ;;
    --mode)       MODE="$2"; shift 2 ;;
    --idea)       IDEA="$2"; shift 2 ;;
    --workdir)    WORKDIR="$2"; shift 2 ;;
    --skip-deploy) SKIP_DEPLOY="true"; shift 1 ;;
    -h|--help)    usage; exit 0 ;;
    *)            echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

# ─── Interactive Setup Wizard ──────────────────────────────────────────────────
run_setup_wizard() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║       🌐  Idle Web Developer — First-Time Setup         ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo ""

  # Step A: Vercel Token (required)
  echo "─── Step 1 of 3: Vercel Token (required) ───────────────"
  echo "To deploy your sites, I need your Vercel token."
  echo "You can find it at: https://vercel.com/account/tokens"
  echo ""
  while true; do
    read -rp "Vercel token: " INPUT_VERCEL_TOKEN
    if [[ -n "$INPUT_VERCEL_TOKEN" ]]; then
      break
    fi
    echo "⚠️  Vercel token is required."
  done

  echo ""

  # Step B: Google Analytics (optional)
  echo "─── Step 2 of 3: Google Analytics (optional) ───────────"
  echo "Enable Google Analytics to track page views across your sites."
  echo ""
  read -rp "Enable Google Analytics? (y/n): " GA_CHOICE
  INPUT_GA_MEASUREMENT_ID=""
  INPUT_GOOGLE_CREDENTIALS=""

  if [[ "$GA_CHOICE" =~ ^[Yy] ]]; then
    read -rp "Google Application Credentials JSON path: " INPUT_GOOGLE_CREDENTIALS
    read -rp "GA4 Measurement ID (e.g. G-XXXXXXXXXX): " INPUT_GA_MEASUREMENT_ID
    echo "✅ Analytics configured."
  else
    echo "⏭️  Analytics skipped."
  fi

  echo ""

  # Step C: Supabase Waitlist (optional)
  echo "─── Step 3 of 3: Supabase Waitlist (optional) ──────────"
  echo "Every site includes a 'Join the Waitlist' section."
  echo "Connect Supabase to actually save email signups."
  echo ""
  read -rp "Enable Supabase waitlist? (y/n): " SB_CHOICE
  INPUT_SUPABASE_URL=""
  INPUT_SUPABASE_ANON_KEY=""

  if [[ "$SB_CHOICE" =~ ^[Yy] ]]; then
    read -rp "Supabase project URL (e.g. https://xxxx.supabase.co): " INPUT_SUPABASE_URL
    read -rp "Supabase anon/public key: " INPUT_SUPABASE_ANON_KEY
    echo "✅ Supabase configured."
    echo ""
    echo "📝 Note: Make sure you have a 'waitlist' table in Supabase:"
    echo "   create table if not exists waitlist ("
    echo "     id uuid default gen_random_uuid() primary key,"
    echo "     email text not null unique,"
    echo "     created_at timestamptz default now()"
    echo "   );"
  else
    echo "⏭️  Supabase skipped — waitlist UI will still appear on every site."
  fi

  echo ""

  # Save config
  cat > "$CONFIG_FILE" <<EOF
VERCEL_TOKEN="${INPUT_VERCEL_TOKEN}"
GOOGLE_APPLICATION_CREDENTIALS="${INPUT_GOOGLE_CREDENTIALS}"
GA_MEASUREMENT_ID="${INPUT_GA_MEASUREMENT_ID}"
SUPABASE_URL="${INPUT_SUPABASE_URL}"
SUPABASE_ANON_KEY="${INPUT_SUPABASE_ANON_KEY}"
EOF

  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║  ✅ Setup complete! Config saved.                    ║"
  echo "║  Re-run anytime with: build-and-deploy.sh --setup   ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo ""
}

# ─── Load or Create Config ────────────────────────────────────────────────────
if [[ "$RUN_SETUP" == "true" ]]; then
  run_setup_wizard
  # If only --setup was passed (no --name), exit after setup
  if [[ -z "$NAME" ]]; then
    exit 0
  fi
elif [[ ! -f "$CONFIG_FILE" ]]; then
  echo "🆕 First time running the Idle Web Developer — starting setup..."
  run_setup_wizard
fi

# Source the config
# shellcheck disable=SC1090
source "$CONFIG_FILE"

# ─── Validate ─────────────────────────────────────────────────────────────────
if [[ -z "$NAME" ]]; then
  echo "Error: --name is required for building."
  usage
  exit 1
fi

if [[ "$MODE" != "static" && "$MODE" != "nextjs" ]]; then
  echo "--mode must be static or nextjs"
  exit 1
fi

if [[ -z "${VERCEL_TOKEN:-}" ]]; then
  echo "❌ VERCEL_TOKEN is not set. Run --setup to configure."
  exit 1
fi

if [[ "$SKIP_DEPLOY" != "true" ]]; then
  if ! command -v vercel >/dev/null 2>&1; then
    echo "❌ Missing Vercel CLI. Install with: npm i -g vercel"
    exit 1
  fi
fi

# ─── Analytics Check ──────────────────────────────────────────────────────────
ANALYTICS_ENABLED="false"
GA_CREDENTIALS_PATH="${GOOGLE_APPLICATION_CREDENTIALS:-}"

if [[ -n "${GA_MEASUREMENT_ID:-}" ]] && \
   ([[ -n "${GA_CREDENTIALS_PATH}" ]] || [[ -f "$HOME/.openclaw/workspace/secrets/ga-service-account.json" ]]); then
  ANALYTICS_ENABLED="true"
  echo "✅ Analytics enabled — Measurement ID: ${GA_MEASUREMENT_ID}"
else
  echo "⚠️  Analytics skipped — set GA_MEASUREMENT_ID and GOOGLE_APPLICATION_CREDENTIALS to enable"
fi

# ─── Supabase Check ───────────────────────────────────────────────────────────
SUPABASE_ENABLED="false"
if [[ -n "${SUPABASE_URL:-}" && -n "${SUPABASE_ANON_KEY:-}" ]]; then
  SUPABASE_ENABLED="true"
  echo "✅ Waitlist wired to Supabase — ${SUPABASE_URL}"
else
  echo "⚠️  Waitlist is UI-only — set SUPABASE_URL and SUPABASE_ANON_KEY to enable real sign-ups"
fi

# ─── Build ────────────────────────────────────────────────────────────────────
TARGET_DIR="${WORKDIR%/}/${NAME}"
mkdir -p "$TARGET_DIR"

# ── GA snippet helper ──────────────────────────────────────────────────────────
ga_snippet() {
  if [[ "$ANALYTICS_ENABLED" == "true" ]]; then
    cat <<GASNIPPET
  <script async src="https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${GA_MEASUREMENT_ID}', { page_title: document.title, page_location: location.href });
    gtag('event', 'page_view', { product_id: location.hostname });
  </script>
GASNIPPET
  fi
}

# ── Waitlist inline script helper ─────────────────────────────────────────────
waitlist_script() {
  if [[ "$SUPABASE_ENABLED" == "true" ]]; then
    cat <<SBSCRIPT
    <script>
      document.getElementById('waitlist-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        var email = document.getElementById('waitlist-email').value;
        var btn = document.getElementById('waitlist-btn');
        var msg = document.getElementById('waitlist-msg');
        btn.disabled = true;
        btn.textContent = 'Joining...';
        try {
          var res = await fetch('${SUPABASE_URL}/rest/v1/waitlist', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'apikey': '${SUPABASE_ANON_KEY}',
              'Authorization': 'Bearer ${SUPABASE_ANON_KEY}',
              'Prefer': 'return=minimal'
            },
            body: JSON.stringify({ email: email })
          });
          if (res.ok || res.status === 409) {
            document.getElementById('waitlist-form').style.display = 'none';
            msg.style.display = 'block';
          } else {
            btn.disabled = false;
            btn.textContent = 'Notify Me';
            alert('Something went wrong. Please try again.');
          }
        } catch(err) {
          btn.disabled = false;
          btn.textContent = 'Notify Me';
          alert('Network error. Please try again.');
        }
      });
    </script>
SBSCRIPT
  else
    cat <<PLACEHOLDER
    <script>
      document.getElementById('waitlist-form').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('waitlist-form').style.display = 'none';
        document.getElementById('waitlist-msg').style.display = 'block';
      });
    </script>
PLACEHOLDER
  fi
}

# ─── Static Mode ──────────────────────────────────────────────────────────────
if [[ "$MODE" == "static" ]]; then
  cat > "${TARGET_DIR}/index.html" <<HTML
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1.0" />
  <title>${NAME}</title>
  <style>
    :root { color-scheme: dark; }
    *, *::before, *::after { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: radial-gradient(1000px 500px at 80% -10%, #3b82f6 0%, transparent 60%), #0b1020;
      color: #e8ecff;
      min-height: 100vh;
    }

    /* Nav */
    nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 16px 32px;
      background: rgba(11,16,32,0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .nav-brand { font-weight: 700; font-size: 1.1rem; }
    .nav-cta {
      background: #4f7cff; color: white; text-decoration: none;
      border-radius: 10px; padding: 8px 20px; font-weight: 600; font-size: 0.9rem;
    }

    /* Hero */
    .hero {
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
      text-align: center; padding: 100px 24px 60px;
    }
    .hero-inner { max-width: 760px; }
    h1 { margin: 0 0 16px; font-size: clamp(2.2rem, 5vw, 3.8rem); line-height: 1.15; }
    .hero p { margin: 0 0 32px; color: #b8c2f0; font-size: 1.15rem; line-height: 1.7; }
    .btn {
      display: inline-block; background: #4f7cff; color: white; text-decoration: none;
      border-radius: 14px; padding: 14px 32px; font-weight: 700; font-size: 1rem;
      transition: transform 0.15s, box-shadow 0.15s;
    }
    .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(79,124,255,0.4); }

    /* Sections */
    section { padding: 80px 24px; max-width: 960px; margin: 0 auto; }
    h2 { font-size: clamp(1.6rem, 3vw, 2.4rem); margin: 0 0 12px; text-align: center; }
    .sub { color: #b8c2f0; text-align: center; margin: 0 0 48px; font-size: 1.05rem; }

    /* Features */
    .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; }
    .feature-card {
      background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px; padding: 28px 24px;
    }
    .feature-card h3 { margin: 0 0 8px; font-size: 1.1rem; }
    .feature-card p { margin: 0; color: #b8c2f0; font-size: 0.95rem; line-height: 1.6; }

    /* Waitlist */
    .waitlist-band {
      background: rgba(79,124,255,0.08);
      border-top: 1px solid rgba(79,124,255,0.2);
      border-bottom: 1px solid rgba(79,124,255,0.2);
      padding: 80px 24px;
      text-align: center;
    }
    .waitlist-band h2 { margin: 0 0 12px; }
    .waitlist-band .sub { margin: 0 0 36px; }
    #waitlist-form { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
    #waitlist-email {
      padding: 14px 20px; border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.06); color: #e8ecff;
      font-size: 1rem; width: min(320px, 100%);
      outline: none;
    }
    #waitlist-email:focus { border-color: #4f7cff; }
    #waitlist-btn {
      padding: 14px 28px; background: #4f7cff; color: white;
      border: none; border-radius: 12px; font-weight: 700; font-size: 1rem;
      cursor: pointer; transition: transform 0.15s;
    }
    #waitlist-btn:hover:not(:disabled) { transform: translateY(-2px); }
    #waitlist-btn:disabled { opacity: 0.6; cursor: not-allowed; }
    #waitlist-msg { display: none; color: #6ee7b7; font-size: 1.1rem; font-weight: 600; }

    /* Footer */
    footer {
      text-align: center; padding: 32px 24px;
      color: #5a6580; font-size: 0.85rem;
      border-top: 1px solid rgba(255,255,255,0.06);
    }
  </style>
</head>
<body>

  <nav>
    <span class="nav-brand">${NAME}</span>
    <a class="nav-cta" href="#waitlist">Get Early Access</a>
  </nav>

  <!-- Hero -->
  <div class="hero">
    <div class="hero-inner">
      <h1>${NAME}</h1>
      <p>${IDEA:-A polished product built for the people who need it most.}</p>
      <a class="btn" href="#waitlist">Join the Waitlist</a>
    </div>
  </div>

  <!-- Features -->
  <section>
    <h2>Why ${NAME}?</h2>
    <p class="sub">Built for the people who need it most.</p>
    <div class="features-grid">
      <div class="feature-card">
        <h3>⚡ Fast</h3>
        <p>Designed from the ground up for speed — no bloat, no noise.</p>
      </div>
      <div class="feature-card">
        <h3>🎯 Focused</h3>
        <p>Purpose-built for your workflow. Nothing you don't need.</p>
      </div>
      <div class="feature-card">
        <h3>🔒 Private</h3>
        <p>Your data stays yours. No tracking, no selling, no surprises.</p>
      </div>
    </div>
  </section>

  <!-- Waitlist -->
  <div class="waitlist-band" id="waitlist">
    <h2>Be the First to Know</h2>
    <p class="sub">Drop your email and we'll reach out the moment we launch.</p>
    <form id="waitlist-form">
      <input type="email" id="waitlist-email" placeholder="your@email.com" required />
      <button type="submit" id="waitlist-btn">Notify Me</button>
    </form>
    <p id="waitlist-msg">✅ You're on the list! We'll be in touch soon.</p>
  </div>

  <!-- Footer -->
  <footer>
    <p>© $(date +%Y) ${NAME}. All rights reserved.</p>
  </footer>

$(waitlist_script)
$(ga_snippet)
</body>
</html>
HTML

# ─── Next.js Mode ─────────────────────────────────────────────────────────────
elif [[ "$MODE" == "nextjs" ]]; then
  if [[ -n "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]]; then
    echo "❌ Target directory is not empty: $TARGET_DIR"
    echo "Use a fresh --name or clean the directory first."
    exit 1
  fi

  npx create-next-app@latest "$TARGET_DIR" --ts --tailwind --eslint --app --use-npm --yes

  # Write Waitlist component
  mkdir -p "${TARGET_DIR}/src/components"
  cat > "${TARGET_DIR}/src/components/Waitlist.tsx" <<WAITLISTtsx
'use client';
import { useState } from 'react';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? '';
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '';
const SUPABASE_ENABLED = !!(SUPABASE_URL && SUPABASE_ANON_KEY);

export default function Waitlist() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'done' | 'error'>('idle');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('loading');
    if (SUPABASE_ENABLED) {
      try {
        const res = await fetch(\`\${SUPABASE_URL}/rest/v1/waitlist\`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            apikey: SUPABASE_ANON_KEY,
            Authorization: \`Bearer \${SUPABASE_ANON_KEY}\`,
            Prefer: 'return=minimal',
          },
          body: JSON.stringify({ email }),
        });
        setStatus(res.ok || res.status === 409 ? 'done' : 'error');
      } catch {
        setStatus('error');
      }
    } else {
      // Placeholder mode — always succeed
      setStatus('done');
    }
  }

  return (
    <section id="waitlist" className="py-20 px-6 text-center bg-blue-500/5 border-y border-blue-500/20">
      <h2 className="text-3xl font-bold mb-3">Be the First to Know</h2>
      <p className="text-gray-400 mb-8">Drop your email and we'll reach out the moment we launch.</p>
      {status === 'done' ? (
        <p className="text-green-400 font-semibold text-lg">✅ You're on the list! We'll be in touch soon.</p>
      ) : (
        <form onSubmit={handleSubmit} className="flex gap-3 justify-center flex-wrap">
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="your@email.com"
            required
            className="px-5 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 w-72"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-7 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl transition disabled:opacity-60"
          >
            {status === 'loading' ? 'Joining...' : 'Notify Me'}
          </button>
          {status === 'error' && (
            <p className="w-full text-red-400 text-sm mt-2">Something went wrong. Please try again.</p>
          )}
        </form>
      )}
    </section>
  );
}
WAITLISTtsx

  # Write .env.local for Next.js
  cat > "${TARGET_DIR}/.env.local" <<ENVLOCAL
NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
ENVLOCAL

  echo "📦 Next.js app scaffolded with Waitlist component."
fi

# ─── Skip Deploy ──────────────────────────────────────────────────────────────
cd "$TARGET_DIR"

if [[ "$SKIP_DEPLOY" == "true" ]]; then
  echo ""
  echo "🧪 Scaffold complete (deploy skipped)"
  echo "📁 Folder: $TARGET_DIR"
  echo ""
  echo "Summary:"
  echo "  Analytics : $( [[ "$ANALYTICS_ENABLED" == "true" ]] && echo "✅ enabled (${GA_MEASUREMENT_ID})" || echo "⏭️  skipped" )"
  echo "  Waitlist  : $( [[ "$SUPABASE_ENABLED" == "true" ]] && echo "✅ wired to Supabase (${SUPABASE_URL})" || echo "⏭️  UI-only placeholder" )"
  exit 0
fi

# ─── Deploy ───────────────────────────────────────────────────────────────────
# Deploy pre-built output (not source) — Vercel server rebuild won't have env vars
if [[ -d "dist" ]]; then
  # Tell Vercel: skip server-side build, serve static files as-is
  cat > dist/vercel.json <<'VJSON'
{ "buildCommand": "", "outputDirectory": "." }
VJSON
  DEPLOY_DIR="dist/"
else
  DEPLOY_DIR="."
fi
DEPLOY_URL="$(vercel deploy "${DEPLOY_DIR}" --prod --yes --token "${VERCEL_TOKEN}")"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Deployed!                                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  URL       : $DEPLOY_URL"
echo "  Folder    : $TARGET_DIR"
echo "  Analytics : $( [[ "$ANALYTICS_ENABLED" == "true" ]] && echo "✅ enabled (${GA_MEASUREMENT_ID})" || echo "⏭️  skipped" )"
echo "  Waitlist  : $( [[ "$SUPABASE_ENABLED" == "true" ]] && echo "✅ wired to Supabase" || echo "⏭️  UI-only placeholder" )"

if [[ "$SUPABASE_ENABLED" == "true" ]]; then
  echo ""
  echo "📝 Supabase reminder: ensure 'waitlist' table exists:"
  echo "   create table if not exists waitlist ("
  echo "     id uuid default gen_random_uuid() primary key,"
  echo "     email text not null unique,"
  echo "     created_at timestamptz default now()"
  echo "   );"
fi
