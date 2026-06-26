Curated Prompts

- Run `runner.sh gpu status --json` and summarize pod state.
- Run `runner.sh gpu inventory --json --available --max-price 0.50` and suggest a GPU for FLUX.
- Run `runner.sh gpu run python train.py --gpu-type "RTX 4090"` with batch size 4; preview the plan.
- Run `runner.sh gpu comfyui run flux_schnell` and sync images to outputs/.
- Run `runner.sh gpu llm run --vllm --model llama-3.1-8b-instruct -y -p 8000:8000`.

Notes
- The skill enforces a single 'runner.sh gpu …' command with no shell chaining or redirection.
- Dry-run is on by default; set `SKILL_DRY_RUN=false` and `SKILL_CONFIRM=yes` to execute.
