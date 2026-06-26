# Phase 6 — RunPod LoRA Training

## Input Contract

- User has uploaded or produced a ZIP file with dataset structure: `{repeats}_{FullName} {class}/`
- Each subfolder contains `.png` images and `.txt` caption files
- `runpodctl` is installed and configured, SSH key registered
- RunPod credits available

## Output Contract

- `.safetensors` LoRA model file(s) downloaded to `~/.openclaw/workspace/lora_outputs/<timestamp>/`
- Pod is stopped to prevent idle charges
- User notified with output file paths

## Completion Signal

```
sessions_send(parent_session_id, "✅ Phase 6 complete: LoRA training done. Outputs at ~/.openclaw/workspace/lora_outputs/<timestamp>/. Files: <list>. Pod <POD_ID> stopped.")
```

Fallback: write to `~/.openclaw/workspace/lora_status_phase6.txt`

## Model Recommendation

`openrouter/google/gemini-2.0-flash-lite-001` (Worker) + Sentry sub-agent for monitoring (see Sentry section below)

---

## 🛡️ Privacy & Security (CRITICAL)

- **NO DATA INSPECTION**: Do NOT `cat`, `read`, or analyze image or `.txt` caption files.
- **NO DATA LEAKAGE**: Do not describe dataset contents to the LLM.
- **SYSTEM-ONLY ACTIONS**: Only file-level operations (listing counts, transfer, existence checks).

---

## Default Pod Parameters

| Parameter | Value |
|-----------|-------|
| GPU | `NVIDIA RTX A5000` |
| Template ID | `uajca40f1z` |
| Image | `ashleykza/kohya:cu124-py311-25.2.1` |
| Container Disk | `20` GB |
| Volume Size | `0` GB (No Volume) |
| Secure Cloud | `true` (ALWAYS `--cloud-type SECURE`) |
| Preferred Zones | `EU` (Romania, Germany, etc.) |
| Restricted Zones | DO NOT USE `CA` (Canada) |

---

## Full Workflow

### Step 1 — Main Agent: Pre-check & Confirm

**Trigger:** User uploads a ZIP file and asks to train a LoRA.

1. **Extract the ZIP** to a temp directory:
   ```bash
   EXTRACT_DIR=~/.openclaw/workspace/lora_staging/$(date +%Y%m%d_%H%M%S)
   mkdir -p "$EXTRACT_DIR"
   unzip /path/to/uploaded.zip -d "$EXTRACT_DIR"
   ```

2. **Validate folder structure** inside the extracted directory. Expect folders matching `{number}_{full name} {class}`:
   ```bash
   ls "$EXTRACT_DIR"
   # Expected: 50_DerekLunsford man/, 50_JaneDoe woman/, etc.
   ```
   - Ensure folder name contains the **full name** and **class** (man, woman, person).
   - Each folder should contain images and `.txt` captions.
   - If structure is incomplete, inform the user and suggest correct format before proceeding.

3. **Reply to user** with summary and wait for confirmation:
   ```
   Found X dataset folder(s):
   - 50_person1 (N images)
   ...

   Default RunPod parameters:
   - GPU: NVIDIA RTX A5000
   - Template: uajca40f1z
   - Secure Cloud: enabled

   Estimated time: ~10–20 min per dataset on A5000
   This will use RunPod credits. Proceed?
   ```

4. **Wait for user confirmation** before spawning sub-agent.

---

### Step 2 — Main Agent: Spawn Sub-Agent

Once user confirms, spawn a Sub-Agent. Do NOT run inline — it blocks main chat for 30+ minutes.

```
Use sessions_spawn with:
  model: openrouter/google/gemini-2.0-flash-lite-001
  label: lora-trainer-{timestamp}
  context:
    - EXTRACT_DIR path
    - ZIP file path
    - Requester session ID (for sessions_send callback)
```

Tell the user: "Training has started in the background. I'll notify you when it's done."

---

### Step 3 — Sub-Agent: Create Pod

```bash
runpodctl pod create \
  --name "lora-trainer-$(date +%Y%m%d%H%M%S)" \
  --template-id "uajca40f1z" \
  --gpu-id "NVIDIA RTX A5000" \
  --cloud-type SECURE
```

> **CRITICAL:**
> 1. Use `--template-id` (not `--image`) to ensure Web UI ports are correctly mapped.
> 2. Do NOT specify `--volume-in-gb` unless explicitly requested (causes "no instances available" errors).
> 3. Avoid `CA` data centers.
> 4. After creation, use `runpodctl pod get <POD_ID> --output=yaml` to extract SSH IP/port.

---

### Step 4 — Sub-Agent: Wait for Pod Ready

Poll until running, then SSH:

```bash
runpodctl pod get <POD_ID> --output=yaml
runpodctl ssh info <POD_ID>
```

Wait until `runpodctl ssh info` returns a valid SSH command (contains `ssh -p`).

**Waiting rules:**
- If actively pulling image → extend timeout up to **10 minutes** (large images take time)
- Check every 20 seconds
- If stuck on real error or exceeds timeout → `runpodctl pod delete <POD_ID>` immediately (stop billing)
- Report failure + last known status/log to main session

Parse SSH details:
```bash
SSH_CMD=$(runpodctl ssh info <POD_ID>)
SSH_PORT=$(echo "$SSH_CMD" | awk '{for(i=1;i<=NF;i++) if($i=="-p") print $(i+1)}')
SSH_HOST=$(echo "$SSH_CMD" | awk '{for(i=1;i<=NF;i++) if($i~/@/) {split($i,a,"@"); print a[2]}}')
SSH_KEY=$(echo "$SSH_CMD" | awk '{for(i=1;i<=NF;i++) if($i=="-i") print $(i+1)}')
```

---

### Step 5 — Sub-Agent: Upload Datasets & Script

```bash
# Upload dataset subfolders directly into /workspace/datasets/
scp -P "$SSH_PORT" -i "$SSH_KEY" \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile=~/.runpod/ssh/known_hosts \
    -r "$EXTRACT_DIR"/* \
    root@${SSH_HOST}:/workspace/datasets/

# Upload training script
scp -P "$SSH_PORT" -i "$SSH_KEY" \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile=~/.runpod/ssh/known_hosts \
    ~/.openclaw/skills/lora-pipeline/scripts/batch_lora_train.py \
    root@${SSH_HOST}:/workspace/batch_lora_train.py
```

> **CRITICAL:** Use `"$EXTRACT_DIR"/*` (with asterisk) to copy subfolders directly into `/workspace/datasets/`. Avoid nested paths like `/workspace/datasets/20260314_staging/50_derek/`.

---

### Step 6 — Sub-Agent: Run Training + Sentry

```bash
ssh -p "$SSH_PORT" root@"$SSH_HOST" \
    -i "$SSH_KEY" \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile=~/.runpod/ssh/known_hosts \
    "cd /workspace && echo y | nohup python3 /workspace/batch_lora_train.py > /workspace/training.log 2>&1 &"
```

**Spawn Sentry sub-agent (bash-only polling, zero LLM calls during wait):**

```
Use sessions_spawn with:
  model: openrouter/google/gemini-2.0-flash-lite-001
  label: lora-sentry-{pod_id}
  task: |
    Monitor training using BASH-ONLY polling. Do NOT use LLM reasoning for each check.
    Run the following bash loop:

    for i in $(seq 1 40); do
      STATUS=$(ssh -p $SSH_PORT root@$SSH_HOST -i $SSH_KEY \
        -o StrictHostKeyChecking=accept-new \
        -o UserKnownHostsFile=~/.runpod/ssh/known_hosts "
        if ls /workspace/kohya_ss/outputs/*.safetensors 2>/dev/null | grep -q .; then
          echo 'DONE'
        elif grep -q '❌' /workspace/training.log 2>/dev/null; then
          echo 'ERROR'
        elif grep -q 'CUDA out of memory' /workspace/training.log 2>/dev/null; then
          echo 'OOM'
        else
          echo 'RUNNING'
        fi
      " 2>/dev/null || echo 'SSH_FAIL')

      if [ "$STATUS" = "DONE" ] || [ "$STATUS" = "ERROR" ] || [ "$STATUS" = "OOM" ]; then
        break
      fi
      sleep 30
    done
    # Max 40 × 30s = 20 minutes

    After loop: send ONE sessions_send to parent with STATUS + last 20 lines of training.log
    If DONE: list .safetensors in /workspace/kohya_ss/outputs/
```

> **QUOTA PROTECTION RULES:**
> - Bash loop uses **zero LLM API calls** — all checks are pure `ssh` + `grep`
> - Poll interval: `sleep 30`
> - Max: 40 iterations = **20 minutes** then auto-exit
> - Sentry makes exactly **1 LLM call total**: to send the final `sessions_send`
> - If sentry's API call fails → write status to `~/.openclaw/workspace/lora_status_{pod_id}.txt` as fallback

> **NO ESCALATION — ABSOLUTE RULE:** Sentry stays on `openrouter/google/gemini-2.0-flash-lite-001` always.
> Prohibited models: Sonnet, Opus, or any higher-tier variant.
> On error → send plain-text alert to parent session. Let parent decide.

---

### Step 7 — Sub-Agent: Retrieve Outputs

```bash
LOCAL_OUTPUT=~/.openclaw/workspace/lora_outputs/$(date +%Y%m%d_%H%M%S)
mkdir -p "$LOCAL_OUTPUT"

scp -P "$SSH_PORT" -i "$SSH_KEY" \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile=~/.runpod/ssh/known_hosts \
    "root@${SSH_HOST}:/workspace/kohya_ss/outputs/*.safetensors" \
    "$LOCAL_OUTPUT/"

ls -lh "$LOCAL_OUTPUT/"
```

After verifying files exist locally → **stop the pod immediately** to prevent idle charges.

---

### Step 8 — Sub-Agent: Notify & Cleanup

```
sessions_send(parent_session_id,
  "✅ LoRA training complete!\n\nOutputs: {LOCAL_OUTPUT}\nFiles: {list}\n\nPod {POD_ID} stopped.\nDelete pod + staging files?")
```

**Autonomy rules:**
- Do NOT ask "Should I download now?" — just download when training succeeds
- Do NOT ask "Should I stop the pod?" — stop it immediately after files are safe locally
- Report actions, don't request them for routine success paths

---

## Dataset Layout on Pod

```
/workspace/datasets/
├── 50_DerekLunsford man/
│   ├── image001.png
│   ├── image001.txt    # DerekLunsford, 1boy, muscular, ...
│   └── ...
└── 50_JaneDoe woman/
    └── ...
```

Outputs named by stripping class word:
- `50_DerekLunsford man/` → `DerekLunsford_lora.safetensors`

---

## Training Parameters (defaults in script)

| Parameter | Value |
|-----------|-------|
| Base model | runwayml/stable-diffusion-v1-5 |
| Resolution | 512×512 |
| Batch size | 4 (A5000 OOM-safe) |
| Max train steps | 600 |
| Learning rate | 0.0002 |
| Network dim | 64 |
| Network alpha | 32 |
| Optimizer | AdamW8bit |
| Mixed precision | fp16 |
| LR scheduler | cosine |

To change: edit `skills/lora-pipeline/scripts/batch_lora_train.py` → `TRAIN_CONFIG` section before uploading.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Pod creation fails | Report to main session; do NOT retry automatically |
| SSH not available after 5 min | Stop pod, report failure |
| SCP upload fails | Report error; pod may still be running — prompt user to clean up |
| Training fails (non-zero exit) | Check if any `.safetensors` produced; report partial results |
| No outputs found | Report failure; notify main session for cleanup decision |

---

## Cost Estimates

- A5000 (~$0.22/hr on secure cloud)
- Upload + setup: ~2–3 min
- Training: ~10–20 min per dataset
- 3 datasets ≈ ~1 hour ≈ ~$0.22

Always stop/remove pod after training to avoid idle charges.
