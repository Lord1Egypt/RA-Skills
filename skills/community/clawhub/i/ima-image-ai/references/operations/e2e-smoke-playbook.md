# E2E Smoke Playbook

Local checks:

1. `python3 scripts/ima_runtime_setup.py`
2. `python3 scripts/ima_runtime_doctor.py`
3. `python3 scripts/ima_runtime_cli.py --help`
4. `python3 -m unittest discover tests -v`

Live checks with a real API key:

1. `python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json`
2. one `text_to_image` happy-path generation without `--model-id`
3. one `image_to_image` happy-path generation using either a local file upload or the HTTPS URL returned by step 2

Copy-paste live smoke sequence:

```bash
python3 scripts/ima_runtime_doctor.py --output-json
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
MODEL_ID="$(python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["model_id"])')"
TEXT_TO_IMAGE_JSON="$(python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --model-id "$MODEL_ID" \
  --size 512px \
  --prompt "simple geometric poster, blue circle on cream background" \
  --output-json)"
printf '%s\n' "$TEXT_TO_IMAGE_JSON"
IMAGE_URL="$(printf '%s' "$TEXT_TO_IMAGE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["url"])')"
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images "$IMAGE_URL" \
  --prompt "turn this into a watercolor illustration" \
  --output-json
```
