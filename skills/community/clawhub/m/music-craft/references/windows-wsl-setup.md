# Windows + WSL2 Setup for Local Models

This reference covers running the **local** ACE-Step backend on Windows. It is
the detailed walkthrough behind the short Windows decision flow in `SKILL.md`.

It covers native Windows vs WSL2 decisions, CUDA passthrough, model downloads,
proxy/certificate troubleshooting, and the local ACE-Step API workflow.

## Read this first: native Windows vs WSL2 vs cloud

- **Cloud backends** (MiniMax `mmx`, Stable Audio) need no WSL and no GPU, but
  require provider accounts, API keys, and network access to the provider.
- **Local models (ACE-Step) on native Windows** are NOT recommended. PyTorch+CUDA
  work natively, but ACE-Step's setup scripts are bash, and the experience the
  author validated is the Linux one. Use WSL2 instead.
- **Local models via WSL2** is the supported path. WSL2 gives a real Linux with
  CUDA passthrough to your NVIDIA GPU. This is what the rest of this file covers.

Note on "cover": MiniMax is still the fast cloud cover path. ACE-Step also has
a local audio-conditioned `cover` mode, but on Windows this means WSL2 + CUDA,
longer wall time, and strict timeout/cache handling. Treat local cover as an
experimental path and set expectations with the user before uploading or
generating from source audio.

## Consent protocol (applies to every step here)

WSL setup installs software, downloads many GB, and may require certificate or
proxy configuration on managed networks. Treat all of it as REQUIRED-but-ask:

- Before each install/download, tell the user what it does and its rough size.
  Never auto-install. If the user declines a REQUIRED item, stop and say the
  workflow cannot proceed.
- Ask once, up front, **where to save generated songs** (`OUTPUT_DIR`) and use a
  per-song subfolder. Do not invent a path silently.
- On a shared or managed machine, never modify or reuse existing WSL distros or the
  global `%USERPROFILE%\.wslconfig`. Create a dedicated distro (below).

## Step 1 - Probe Windows from PowerShell (before WSL exists)

The hardware probe in `SKILL.md` is bash and cannot run on native Windows. Use
this PowerShell probe instead:

```powershell
(Get-CimInstance Win32_OperatingSystem).Caption
[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)  # RAM GB
(Get-CimInstance Win32_Processor).Name
(Get-CimInstance Win32_VideoController).Name                                       # GPUs
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) { 'nvidia-smi present' }
wsl --status; wsl --list --verbose; wsl --version                                 # WSL state
foreach ($t in 'python','uv','git') { if (Get-Command $t -ErrorAction SilentlyContinue) { "$t present" } }
Get-PSDrive C | Select-Object @{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}}        # need ~25-30 GB free
```

A dedicated NVIDIA GPU (even a 12 GB laptop GPU) is the bottleneck pool and is
fine for the standard tier. No NVIDIA GPU means CPU-only (very slow) - prefer
cloud in that case.

## Step 2 - Decide the WSL path (and protect existing distros)

Read `wsl --list --verbose`:

- **No WSL** -> install WSL2 (`wsl --install`, reboot), then continue.
- **WSL present, version 2 available** -> good. Do NOT reuse an existing distro
  unless the user explicitly wants that. Create a dedicated distro for music
  generation.
- **Only a WSL1 distro** -> do NOT convert it (`--set-version` changes networking
  and can break things that rely on it). Install a fresh WSL2 distro instead.

Hard rules on a shared or managed machine:
- Never edit `%USERPROFILE%\.wslconfig` - it is global to all WSL2 distros. On
  some setups it carries networking settings other tools depend on.
- Never touch an existing managed distro without explicit user approval.

## Step 3 - Create a dedicated WSL2 distro (non-interactive)

`wsl --install` normally launches an interactive first-run (username/password)
that will hang an automated shell. Use `--no-launch` and provision as root:

```powershell
wsl --install Ubuntu-24.04 --name acestep --no-launch
wsl --list --verbose            # confirm 'acestep' shows VERSION 2
```

Run everything in the dedicated distro as root: `wsl -d acestep -u root -- <cmd>`.
Running as root in a throwaway sandbox distro is acceptable here.

## Step 4 - Verify GPU passthrough (fail fast here)

Do this BEFORE any large download. If the GPU is not visible, rethink (CPU/cloud):

```bash
nvidia-smi      # must list your NVIDIA GPU with CUDA version
```

## Step 5 - Toolchain, uv, clone, sync

```bash
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git curl ffmpeg python3 python3-pip python3-venv build-essential
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
git clone --depth 1 https://github.com/ace-step/ACE-Step-1.5.git /root/ACE-Step-1.5
cd /root/ACE-Step-1.5 && uv sync     # pulls PyTorch CUDA stack, ~4-5 GB
.venv/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

`uv sync` builds the bundled `nano-vllm` LM backend, so there is no external vLLM
dependency to fight (this is why native-Windows vLLM concerns do not apply here).

## Step 6 - TLS/certificate troubleshooting

HuggingFace serves large model weights from a separate Xet CDN
(`cas-bridge.xethub.hf.co`). On some managed networks, TLS inspection can
replace the upstream certificate, so downloads fail with:

```
SSLError: CERTIFICATE_VERIFY_FAILED: unable to get local issuer certificate
```

`huggingface.co` itself often passes through untouched, which is misleading - the
**weights** still fail. Diagnose which CA is intercepting:

```bash
echo | openssl s_client -connect cas-bridge.xethub.hf.co:443 \
  -servername cas-bridge.xethub.hf.co 2>/dev/null | openssl x509 -noout -issuer
# issuer=... <managed network root CA>  -> interception confirmed
```

Fix: install the relevant trusted root CA (already trusted by Windows) into the
distro.

Export it from Windows (PowerShell), writing a PEM the distro can read:

```powershell
$out = "$env:USERPROFILE\trusted-root-ca.crt"
$certs = Get-ChildItem Cert:\LocalMachine\Root, Cert:\LocalMachine\CA |
  Where-Object { $_.Subject -like '*<certificate authority name>*' -or $_.Issuer -like '*<certificate authority name>*' } |
  Sort-Object Thumbprint -Unique
$sb = New-Object System.Text.StringBuilder
foreach ($c in $certs) {
  [void]$sb.AppendLine('-----BEGIN CERTIFICATE-----')
  [void]$sb.AppendLine([Convert]::ToBase64String($c.RawData,'InsertLineBreaks'))
  [void]$sb.AppendLine('-----END CERTIFICATE-----')
}
Set-Content -Path $out -Value $sb.ToString() -Encoding ascii
```
(Replace `<certificate authority name>` with the relevant trusted root CA name.
Do NOT commit exported certificates to any repo.)

Install it in the distro and point Python at the system bundle:

```bash
# copy the PEM in (from /mnt/c/... or %USERPROFILE%), strip CRLF, split per-cert
tr -d '\r' < /mnt/c/Users/<you>/trusted-root-ca.crt > /tmp/trusted-root-ca.pem
awk '/BEGIN CERTIFICATE/{n++} /BEGIN CERTIFICATE/,/END CERTIFICATE/{print > ("/usr/local/share/ca-certificates/trusted-root-" n ".crt")}' /tmp/trusted-root-ca.pem
update-ca-certificates
# verify
echo | openssl s_client -connect cas-bridge.xethub.hf.co:443 \
  -servername cas-bridge.xethub.hf.co -CAfile /etc/ssl/certs/ca-certificates.crt 2>&1 \
  | grep "verify return code"      # expect: 0 (ok)
```

Then for every Python/HF command, export these if Python still uses a certificate
bundle that lacks the relevant root:

```bash
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export HF_HUB_DISABLE_XET=1      # use the requests path that honors the CA bundle
```

## Step 7 - Proxy env vars can hijack localhost

On a proxied machine, WSL may inherit `HTTP_PROXY`/`http_proxy`. Requests to the
local ACE-Step API (`127.0.0.1:8001`) can then get routed to a proxy and fail.
Bypass the proxy for local calls:

```bash
unset HTTP_PROXY http_proxy HTTPS_PROXY https_proxy ALL_PROXY all_proxy
export no_proxy="127.0.0.1,localhost"; export NO_PROXY="127.0.0.1,localhost"
```
In Python, also set `requests.Session().trust_env = False` for local API calls.

## Step 8 - Download models (consent gate: ~10 GB)

```bash
python -m acestep.model_downloader --list     # show available models
python -m acestep.model_downloader            # main model = standard tier
                                              # (turbo 2B DiT + 1.7B LM + VAE + text encoder)
```

Tiers vs a 12 GB GPU: the **standard** tier (turbo DiT + 1.7B LM, ~8 GB resident)
fits and is the recommended default. The XL tiers need much more VRAM. If the
1.7B LM OOMs on a smaller GPU, download `acestep-5Hz-lm-0.6B` and use the fast
tier. Models land in `./checkpoints`.

## Step 9 - Start the API server

Do NOT run `start_api_server.sh` from an automated agent - it has interactive
`read` prompts (update check, uv install) that hang. Launch the entry point
directly, in a session that stays alive:

```bash
export ACESTEP_CHECKPOINTS_DIR=/root/ACE-Step-1.5/checkpoints
export ACESTEP_CONFIG_PATH=acestep-v15-turbo
export ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B   # 0.6B for fast tier
# plus the CA + no_proxy exports from Steps 6-7
cd /root/ACE-Step-1.5 && uv run --no-sync acestep-api --host 127.0.0.1 --port 8001
```

Models lazy-load on first use. Either POST `/v1/init`
(`{"dit_model":"acestep-v15-turbo","lm_model":"acestep-5Hz-lm-1.7B"}`) or just
submit the first generation and let it load. `/health` returns
`models_initialized` so you can poll readiness.

The real endpoints (verified) match the base skill's docs: `POST /release_task`,
`POST /query_result`, `GET /health`, `POST /v1/init`. The `GenerateMusicRequest`
fields match the parameter table (`prompt`, `lyrics`, `audio_duration`, `bpm`,
`key_scale`, `time_signature`, `vocal_language`, `thinking`, `inference_steps`,
`guidance_scale`, `infer_method`).

## Step 10 - Generate and save output

Submit `/release_task`, poll `/query_result`, then collect the audio (the server
writes to an `api_audio` cache dir under the repo). Copy the result into the
`OUTPUT_DIR/<song-slug>/` subfolder you agreed with the user in the consent step,
alongside the prompt text and any analysis JSON.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `CERTIFICATE_VERIFY_FAILED` on `cas-bridge.xethub.hf.co` / modelscope | TLS inspection or missing trusted root CA | Install the relevant trusted root CA (Step 6) + `REQUESTS_CA_BUNDLE`/`SSL_CERT_FILE` + `HF_HUB_DISABLE_XET=1` |
| `/health` returns a 403 HTML page | `HTTP_PROXY` routing localhost to the proxy | Unset proxy vars / set `no_proxy` / `trust_env=False` (Step 7) |
| `acestep-download` gets a few files then "CAS service error" | Xet CDN blocked | Same as TLS fix above |
| Server start hangs with no output | `start_api_server.sh` waiting on a `read` prompt | Launch `acestep-api` directly (Step 9) |
| Background server dies after the launching command returns | WSL reaps `nohup ... &` when the session exits | Keep the launching session alive (run the server as a long-lived foreground process in its own session) |
| Distro shows VERSION 1 | WSL1 (no CUDA) | Install a fresh WSL2 distro; do not convert in place |
| LM OOM on a small GPU | 1.7B LM too large alongside DiT | Use fast tier (`acestep-5Hz-lm-0.6B`) or set `ACESTEP_OFFLOAD_TO_CPU=true` |
