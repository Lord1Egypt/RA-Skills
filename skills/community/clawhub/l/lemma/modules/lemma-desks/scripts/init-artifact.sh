#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_PACKAGE_NAME="lemma-sdk"
POD_ID_ARG=""

usage() {
  cat <<EOF
Usage: ./init-artifact.sh <project-name-or-path> [--pod-id <pod-id>]

Creates a fresh Vite React + TypeScript desk scaffold, installs the published TypeScript SDK,
and wires the standard Lemma desk env contract:
  ${SDK_PACKAGE_NAME}@latest
EOF
}

PROJECT_INPUT="${1:-}"
if [ -z "${PROJECT_INPUT:-}" ] || [ "${PROJECT_INPUT:-}" = "-h" ] || [ "${PROJECT_INPUT:-}" = "--help" ]; then
  usage
  exit 0
fi
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pod-id)
      POD_ID_ARG="${2:-}"
      if [ -z "$POD_ID_ARG" ]; then
        echo "❌ Missing value for --pod-id."
        exit 1
      fi
      shift 2
      ;;
    *)
      echo "❌ Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ "$PROJECT_INPUT" = /* ]]; then
  TARGET_DIR="$PROJECT_INPUT"
else
  TARGET_DIR="$(pwd)/$PROJECT_INPUT"
fi

if [ -e "$TARGET_DIR" ]; then
  echo "❌ Target already exists: $TARGET_DIR"
  exit 1
fi

PROJECT_NAME="$(basename "$TARGET_DIR")"
PROJECT_SLUG="$(printf '%s' "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]._-' '-' | sed 's/^-*//; s/-*$//')"
[ -n "$PROJECT_SLUG" ] || PROJECT_SLUG="lemma-desk"
TARGET_PARENT="$(dirname "$TARGET_DIR")"

RESOLVED_API_URL="${VITE_LEMMA_API_URL:-${LEMMA_BASE_URL:-}}"
RESOLVED_AUTH_URL="${VITE_LEMMA_AUTH_URL:-${LEMMA_AUTH_URL:-}}"
RESOLVED_POD_ID="${POD_ID_ARG:-${VITE_LEMMA_POD_ID:-${LEMMA_POD_ID:-<pod_id>}}}"

mkdir -p "$TARGET_PARENT"
echo "⚡ Scaffolding Vite React + TypeScript desk..."
(
  cd "$TARGET_PARENT"
  npm create vite@latest "$PROJECT_NAME" -- --template react-ts
)
cd "$TARGET_DIR"

mkdir -p scripts src/lib src/components/ui src/screens
cp "$SCRIPT_DIR/bundle-artifact.sh" ./scripts/bundle-artifact.sh
cp "$SCRIPT_DIR/preview-url.sh" ./scripts/preview-url.sh
cp "$SCRIPT_DIR/print-browser-auth-setup.sh" ./scripts/print-browser-auth-setup.sh
chmod +x ./scripts/*.sh

node - <<'EOF' "$PROJECT_NAME" "$PROJECT_SLUG"
const fs = require("node:fs");
const [projectName, projectSlug] = process.argv.slice(2);

const pkgPath = "package.json";
const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
pkg.name = projectSlug;
pkg.scripts = {
  dev: "vite --host 0.0.0.0 --port 5173",
  build: "vite build",
  preview: "vite preview --host 0.0.0.0 --port 4173",
  "preview:url": "bash ./scripts/preview-url.sh",
  "auth:browser": "bash ./scripts/print-browser-auth-setup.sh",
  bundle: "bash ./scripts/bundle-artifact.sh",
};
fs.writeFileSync(pkgPath, `${JSON.stringify(pkg, null, 2)}\n`);

const htmlPath = "index.html";
let html = fs.readFileSync(htmlPath, "utf8");
html = html.replace("<title>Vite + React + TS</title>", `<title>${projectName}</title>`);
fs.writeFileSync(htmlPath, html, "utf8");
EOF

cat > vite.config.ts <<'EOF'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    allowedHosts: true,
  },
  preview: {
    host: "0.0.0.0",
    port: 4173,
    strictPort: true,
    allowedHosts: true,
  },
});
EOF

node - <<'EOF'
const fs = require("node:fs");

function parseJsonc(contents) {
  return JSON.parse(
    contents
      .replace(/\/\*[\s\S]*?\*\//g, "")
      .replace(/^\s*\/\/.*$/gm, "")
      .replace(/,\s*([}\]])/g, "$1"),
  );
}

for (const file of ["tsconfig.app.json", "tsconfig.json"]) {
  if (!fs.existsSync(file)) continue;
  const json = parseJsonc(fs.readFileSync(file, "utf8"));
  json.compilerOptions = json.compilerOptions || {};
  json.compilerOptions.baseUrl = json.compilerOptions.baseUrl || ".";
  json.compilerOptions.paths = {
    ...(json.compilerOptions.paths || {}),
    "@/*": ["./src/*"],
  };
  fs.writeFileSync(file, `${JSON.stringify(json, null, 2)}\n`);
}
EOF

cat > src/lib/client.ts <<'EOF'
import { LemmaClient } from "lemma-sdk";

// Create the client once at module load time.
// NEVER create LemmaClient inside a React component, inside useState, or inside useMemo.
// AuthGuard requires a stable, non-null LemmaClient. Passing undefined causes:
//   TypeError: Cannot read properties of undefined (reading 'auth')
export const client = new LemmaClient({
  apiUrl: import.meta.env.VITE_LEMMA_API_URL,
  authUrl: import.meta.env.VITE_LEMMA_AUTH_URL,
  podId: import.meta.env.VITE_LEMMA_POD_ID,
});

// Convenience getter for code that prefers a function call.
export function getClient(): LemmaClient {
  return client;
}
EOF

cat > src/lib/utils.ts <<'EOF'
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
EOF

cat > src/components/ui/button.tsx <<'EOF'
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold transition-all disabled:pointer-events-none disabled:opacity-50 outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[color:var(--ring)] focus-visible:ring-offset-[color:var(--background)]",
  {
    variants: {
      variant: {
        default:
          "bg-[var(--primary)] text-[var(--primary-foreground)] shadow-[0_12px_30px_rgba(15,23,42,0.14)] hover:brightness-105",
        secondary:
          "bg-[var(--secondary)] text-[var(--secondary-foreground)] hover:bg-[color:var(--secondary-strong)]",
        outline:
          "border border-[var(--border)] bg-[var(--panel)] text-[var(--foreground)] hover:border-[var(--ring)] hover:bg-[var(--panel-strong)]",
        ghost:
          "text-[var(--muted-foreground)] hover:bg-[var(--panel-strong)] hover:text-[var(--foreground)]",
        destructive:
          "bg-[var(--danger)] text-white shadow-[0_12px_30px_rgba(220,38,38,0.16)] hover:brightness-105",
      },
      size: {
        default: "h-11 px-4 py-2",
        sm: "h-9 rounded-lg px-3",
        lg: "h-12 rounded-2xl px-5",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
EOF

cat > src/components/ui/card.tsx <<'EOF'
import * as React from "react";

import { cn } from "@/lib/utils";

export function Card({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-[24px] border border-[var(--border)] bg-[var(--panel)] shadow-[0_18px_60px_rgba(15,23,42,0.08)]",
        className,
      )}
      {...props}
    />
  );
}

export function CardHeader({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-col gap-2 p-6", className)} {...props} />;
}

export function CardTitle({
  className,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h2 className={cn("text-lg font-semibold tracking-tight text-[var(--foreground)]", className)} {...props} />;
}

export function CardDescription({
  className,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("text-sm leading-6 text-[var(--muted-foreground)]", className)} {...props} />;
}

export function CardContent({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("px-6 pb-6", className)} {...props} />;
}
EOF

cat > src/components/ui/input.tsx <<'EOF'
import * as React from "react";

import { cn } from "@/lib/utils";

export const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-11 w-full rounded-xl border border-[var(--border)] bg-[var(--input)] px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none transition placeholder:text-[var(--muted-foreground)] focus-visible:border-[var(--ring)] focus-visible:ring-2 focus-visible:ring-[color:color-mix(in_srgb,var(--ring)_18%,transparent)]",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";
EOF

cat > src/components/ui/textarea.tsx <<'EOF'
import * as React from "react";

import { cn } from "@/lib/utils";

export const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[120px] w-full rounded-xl border border-[var(--border)] bg-[var(--input)] px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none transition placeholder:text-[var(--muted-foreground)] focus-visible:border-[var(--ring)] focus-visible:ring-2 focus-visible:ring-[color:color-mix(in_srgb,var(--ring)_18%,transparent)]",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Textarea.displayName = "Textarea";
EOF

cat > src/main.tsx <<'EOF'
import React from "react";
import ReactDOM from "react-dom/client";

// AuthGuard must be imported from "lemma-sdk/react" — NOT from "lemma-sdk".
// The styles import is required for the built-in sign-in page to render correctly.
import { AuthGuard } from "lemma-sdk/react";
import "lemma-sdk/react/styles.css";

import App from "./App";
// Import the eagerly-created singleton. Do not call new LemmaClient() here.
import { client } from "./lib/client";
import "./index.css";

// Pass the singleton client to AuthGuard.
// AuthGuard handles auth state: loading → unauthenticated (sign-in page) → renders App.
// All API calls inside App will also use this same client instance.
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthGuard client={client}>
      <App />
    </AuthGuard>
  </React.StrictMode>,
);
EOF

cat > src/App.tsx <<'EOF'
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
// When screens need to call the API, import the client singleton directly:
//   import { client } from "@/lib/client";
// Then use it inside the component:
//   const items = await client.records.list("table_name", { limit: 20 });
// Never pass client as a prop through the component tree — just import it where needed.
import { OverviewScreen } from "@/screens/OverviewScreen";
import { SettingsScreen } from "@/screens/SettingsScreen";
import { WorkQueueScreen } from "@/screens/WorkQueueScreen";

type Screen = "overview" | "work" | "settings";

export default function App() {
  const [screen, setScreen] = useState<Screen>("work");
  const navItems: Array<{ id: Screen; label: string }> = [
    { id: "overview", label: "Overview" },
    { id: "work", label: "Work Queue" },
    { id: "settings", label: "Settings" },
  ];

  const screenCopy = useMemo(() => {
    if (screen === "overview") {
      return {
        title: "Overview",
        description: "Use this screen for summaries, health signals, and the high-level state of the workflow.",
      };
    }
    if (screen === "settings") {
      return {
        title: "Settings",
        description: "Use this area for lower-frequency configuration and operational preferences.",
      };
    }
    return {
      title: "Work Queue",
      description: "Use a list-detail layout here for the main repeatable operator workflow.",
    };
  }, [screen]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(37,99,235,0.12),_transparent_28%),linear-gradient(180deg,_#f8fafc_0%,_#eef4ff_100%)] text-[var(--foreground)]">
      <div className="mx-auto flex min-h-screen max-w-[1440px] flex-col gap-6 p-4 sm:p-6">
        <header className="rounded-[28px] border border-white/70 bg-white/78 px-6 py-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur-xl">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--muted-foreground)]">
                Lemma Desk
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
                Desk App
              </h1>
              <p className="mt-3 text-base leading-7 text-[var(--muted-foreground)]">
                Replace the placeholder screens with the real workflow for this pod.
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              {navItems.map((item) => (
                <Button
                  key={item.id}
                  variant={item.id === screen ? "default" : "outline"}
                  onClick={() => setScreen(item.id)}
                >
                  {item.label}
                </Button>
              ))}
            </div>
          </div>
        </header>

        <section className="grid flex-1 gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
          <Card className="border-white/70 bg-white/72">
            <CardHeader>
              <CardTitle>Navigation</CardTitle>
              <CardDescription>
                Use this shell as the starting point for real product navigation.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setScreen(item.id)}
                  className={
                    item.id === screen
                      ? "w-full rounded-2xl border border-[var(--ring)] bg-[var(--panel-strong)] px-4 py-3 text-left text-sm font-semibold text-[var(--foreground)]"
                      : "w-full rounded-2xl border border-transparent px-4 py-3 text-left text-sm text-[var(--muted-foreground)] hover:border-[var(--border)] hover:bg-[var(--panel-strong)] hover:text-[var(--foreground)]"
                  }
                >
                  {item.label}
                </button>
              ))}
            </CardContent>
          </Card>

          <div className="grid gap-6">
            <Card className="border-white/70 bg-white/72">
              <CardHeader>
                <CardTitle>{screenCopy.title}</CardTitle>
                <CardDescription>{screenCopy.description}</CardDescription>
              </CardHeader>
              <CardContent>
                {screen === "overview" ? <OverviewScreen /> : null}
                {screen === "work" ? <WorkQueueScreen /> : null}
                {screen === "settings" ? <SettingsScreen /> : null}
              </CardContent>
            </Card>
          </div>
        </section>
      </div>
    </main>
  );
}
EOF

cat > src/screens/OverviewScreen.tsx <<'EOF'
import { Card, CardContent } from "@/components/ui/card";

export function OverviewScreen() {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      <Card className="border-dashed bg-white/55">
        <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
          Replace with summary metrics or recent activity if this use case needs an overview.
        </CardContent>
      </Card>
      <Card className="border-dashed bg-white/55 lg:col-span-2">
        <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
          Keep this screen lightweight. If the app is primarily queue-driven, overview can stay minimal.
        </CardContent>
      </Card>
    </div>
  );
}
EOF

cat > src/screens/WorkQueueScreen.tsx <<'EOF'
import { Card, CardContent } from "@/components/ui/card";

export function WorkQueueScreen() {
  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)]">
      <Card className="border-dashed bg-white/55">
        <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
          Put the primary table, list, inbox, or chat surface here.
        </CardContent>
      </Card>
      <Card className="border-dashed bg-white/55">
        <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
          Use this panel for details, editing, approvals, or supporting actions.
        </CardContent>
      </Card>
    </div>
  );
}
EOF

cat > src/screens/SettingsScreen.tsx <<'EOF'
import { Card, CardContent } from "@/components/ui/card";

export function SettingsScreen() {
  return (
    <Card className="border-dashed bg-white/55">
      <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
        Keep lower-frequency configuration here instead of mixing it into the main workflow screen.
      </CardContent>
    </Card>
  );
}
EOF

cat > src/index.css <<'EOF'
@import "tailwindcss";
@import "tw-animate-css";

:root {
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  line-height: 1.5;
  font-weight: 400;
  color: #0f172a;
  background: #f8fafc;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  --background: #f8fafc;
  --foreground: #0f172a;
  --muted-foreground: #526277;
  --panel: rgba(255, 255, 255, 0.72);
  --panel-strong: rgba(255, 255, 255, 0.92);
  --primary: #2563eb;
  --primary-foreground: #eff6ff;
  --secondary: #e2e8f0;
  --secondary-strong: #d6dee8;
  --secondary-foreground: #15304f;
  --input: rgba(255, 255, 255, 0.9);
  --border: rgba(148, 163, 184, 0.32);
  --ring: #3b82f6;
  --danger: #dc2626;
}

* {
  box-sizing: border-box;
}

html,
body,
#root {
  min-height: 100%;
}

body {
  margin: 0;
  color: var(--foreground);
  background: var(--background);
}

button,
input,
textarea,
select {
  font: inherit;
}

code {
  font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
  background: rgba(148, 163, 184, 0.14);
  border-radius: 8px;
  padding: 0.1rem 0.35rem;
}
EOF

cat > .env.local.example <<'EOF'
VITE_LEMMA_API_URL=
VITE_LEMMA_AUTH_URL=
VITE_LEMMA_POD_ID=<pod_id>
LEMMA_DESK_DEV_PORT=5173
EOF

cat > .env.local <<EOF
VITE_LEMMA_API_URL=${RESOLVED_API_URL}
VITE_LEMMA_AUTH_URL=${RESOLVED_AUTH_URL}
VITE_LEMMA_POD_ID=${RESOLVED_POD_ID}
LEMMA_DESK_DEV_PORT=5173
EOF

cat > .gitignore <<'EOF'
# dependencies
node_modules/

# local env
.env.local

# build outputs
dist/
bundle.html

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# editor / OS files
.DS_Store
Thumbs.db
EOF

cat > README.md <<EOF
# ${PROJECT_NAME}

Vite React desk scaffold for Lemma.

## Required env

- \`VITE_LEMMA_API_URL\`
- \`VITE_LEMMA_AUTH_URL\`
- \`VITE_LEMMA_POD_ID\`

This init script writes \`.env.local\` from workspace env when available. If the pod id was not passed,
it writes \`<pod_id>\` as a placeholder so you can replace it before running the desk for real.

## Scripts

- \`npm run dev\` starts the desk on port \`5173\`
- \`npm run preview:url\` prints the agent-local URL and the public workspace URL
- \`npm run bundle\` creates \`bundle.html\` using the same env contract as local dev
- \`npm run auth:browser\` prints localStorage-based browser auth setup for local testing

## SDK

This desk should use the published npm package \`${SDK_PACKAGE_NAME}@latest\`.

Do not replace it with a local file dependency or a copied workspace SDK checkout.
EOF

echo "📦 Installing dependencies..."
npm install
npm install "${SDK_PACKAGE_NAME}@latest" class-variance-authority clsx tailwind-merge lucide-react @radix-ui/react-slot
npm install -D tailwindcss @tailwindcss/vite tw-animate-css

echo "✅ Desk scaffold ready at $TARGET_DIR"
echo "📝 Next steps:"
echo "  cd $TARGET_DIR"
if [ "$RESOLVED_POD_ID" = "<pod_id>" ]; then
  echo "  replace <pod_id> in .env.local before using the desk"
fi
if [ -z "$RESOLVED_API_URL" ] || [ -z "$RESOLVED_AUTH_URL" ]; then
  echo "  fill in any blank values in .env.local"
fi
echo "  replace the starter nav/screens in src/App.tsx with the real desk workflow"
echo "  npm run dev"
echo "  npm run preview:url"
echo "  ask the user to test the public preview URL before bundling"
echo "  npm run bundle"
