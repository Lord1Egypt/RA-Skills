#!/usr/bin/env bash
# Staged AI-headshot workflow over the Motu Color Engine HTTP API.
# Usage: headshots.sh <catalog|people|prepare|confirm|start-person|use-person|remove-person|generate|status|download|render|light|export> ...
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
AGENT="motu-mce-skill/1.0"

usage() {
  cat >&2 <<'EOF'
Usage:
  headshots.sh catalog [locale]
  headshots.sh people [limit]
  headshots.sh prepare <input> <work-dir> [--scene ID] [--garment male|female]
      [--skin-base ID] [--smoothing 0..1] [--crop-spec ID]
      [--crop-anchor auto|center|manual] [--crop-rect X,Y,W,H] [--rotation DEG]
  headshots.sh confirm <work-dir>
  headshots.sh start-person <person-reference-id> <work-dir> [--scene ID]
  headshots.sh use-person <work-dir> <person-reference-id>
  headshots.sh remove-person <person-reference-id>
  headshots.sh generate <work-dir> [--scene ID] [--batch-size 1|2|4]
      [--style ID] [--pose ID] [--outfit ID] [--background ID]
      [--ratio 1:1|4:5|3:4] [--framing auto|close_up|half_body|three_quarter]
      [--hair-grooming true|false] [--face-refinement true|false]
  headshots.sh status <work-dir>
  headshots.sh download <work-dir>
  headshots.sh render <work-dir> --candidate ID|ORDINAL --style ID [--locale LOCALE]
  headshots.sh light <work-dir> --candidate ID|ORDINAL [--style natural_dimension|soft_luminous|studio_definition]
      [--strength 0..1] [--render]
  headshots.sh export <work-dir> --candidate ID|ORDINAL [--render]
      [--crop SPEC] [--format jpeg|png|webp] [--quality 70..100]
EOF
  exit 2
}

require_key() {
  if [ -z "${MCE_API_KEY:-}" ]; then
    echo "MCE_API_KEY is required; create an account key with headshot:process scope." >&2
    exit 2
  fi
}

auth=(-H "X-API-Key: ${MCE_API_KEY:-}")

api_json() {
  local method="$1" path="$2" output="$3"
  shift 3
  local code
  code="$(curl -sS -A "$AGENT" -X "$method" "${auth[@]}" "$BASE$path" "$@" -o "$output" -w '%{http_code}')"
  if [[ ! "$code" =~ ^2 ]]; then
    python3 - "$output" "$code" <<'PY'
import json, pathlib, sys
try:
    body = json.loads(pathlib.Path(sys.argv[1]).read_text())
    detail = body.get("detail", body)
except Exception:
    detail = pathlib.Path(sys.argv[1]).read_text(errors="replace")[:1000]
raise SystemExit(f"Headshots API failed (HTTP {sys.argv[2]}): {detail}")
PY
  fi
}

api_download() {
  local path="$1" output="$2" code
  mkdir -p "$(dirname "$output")"
  code="$(curl -sS -A "$AGENT" "${auth[@]}" "$BASE$path" -o "$output" -w '%{http_code}')"
  if [[ ! "$code" =~ ^2 ]]; then
    local error_body
    error_body="$(cat "$output" 2>/dev/null || true)"
    rm -f "$output"
    echo "Headshots download failed (HTTP $code): $error_body" >&2
    exit 1
  fi
}

state_get() {
  python3 - "$1" "$2" <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
value = data
for part in sys.argv[2].split("."):
    value = value.get(part) if isinstance(value, dict) else None
if value is None:
    raise SystemExit(f"missing workflow state: {sys.argv[2]}")
print(value)
PY
}

state_save() {
  python3 - "$1" "$2" "$3" <<'PY'
import json, pathlib, sys
state_path, section, response_path = map(pathlib.Path, (sys.argv[1], sys.argv[2], sys.argv[3]))
state = json.loads(state_path.read_text()) if state_path.exists() else {"version": 1}
response = json.loads(response_path.read_text())
state[str(section)] = response
for key in ("project_id", "preview_id", "reference_id", "job_id", "candidate_id", "render_id", "export_id"):
    if response.get(key):
        state[key] = response[key]
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
PY
}

json_value() {
  python3 - "$1" "$2" <<'PY'
import json, pathlib, sys
value = json.loads(pathlib.Path(sys.argv[1]).read_text())
for part in sys.argv[2].split("."):
    value = value.get(part) if isinstance(value, dict) else None
if value is None:
    raise SystemExit(f"response is missing {sys.argv[2]}")
print(value)
PY
}

resolve_candidate() {
  python3 - "$1" "$2" <<'PY'
import json, pathlib, sys
state = json.loads(pathlib.Path(sys.argv[1]).read_text())
requested = sys.argv[2]
candidates = (state.get("job") or {}).get("candidates") or []
for item in candidates:
    if item.get("candidate_id") == requested or str(item.get("ordinal")) == requested:
        if item.get("status") != "ready" or not item.get("image_url"):
            raise SystemExit(f"candidate {requested} is not ready")
        print(item["candidate_id"])
        raise SystemExit(0)
raise SystemExit(f"candidate not found in saved job state: {requested}")
PY
}

command="${1:-}"
[ -n "$command" ] || usage
shift

case "$command" in
  catalog)
    locale="${1:-en}"
    response="$(mktemp)"
    trap 'rm -f "$response"' EXIT
    api_json GET "/v1/headshots/catalog?locale=$locale" "$response"
    python3 - "$response" <<'PY'
import json, pathlib, sys
d = json.loads(pathlib.Path(sys.argv[1]).read_text())
print(f"batch_sizes={d.get('batch_sizes')} output_ratios={d.get('output_ratios')} credit_per_image={d.get('credit_cost_per_image')}")
for key in ("scenes", "generation_styles", "poses", "outfits", "backgrounds"):
    print(f"\n{key}:")
    for item in d.get(key, []):
        print(f"  {item.get('id',''):<34} {item.get('name','')}")
PY
    ;;

  people)
    require_key
    limit="${1:-20}" response="$(mktemp)"
    trap 'rm -f "$response"' EXIT
    api_json GET "/v1/headshots/person-references?limit=$limit" "$response"
    python3 - "$response" <<'PY'
import json, pathlib, sys
d = json.loads(pathlib.Path(sys.argv[1]).read_text())
for person in d.get("people", []):
    print(person.get("person_reference_id"), person.get("garment_preference") or "-", person.get("last_used_at") or "-")
PY
    ;;

  prepare)
    require_key
    input="${1:?prepare requires an input image}"
    work="${2:?prepare requires a work directory}"
    shift 2
    [ -f "$input" ] || { echo "input not found: $input" >&2; exit 1; }
    scene="" garment="" skin_base="motu_business_neutral" smoothing="0" crop_spec="profile_4x5"
    crop_anchor="auto" crop_rect="" rotation="0"
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --scene) scene="${2:?}"; shift 2 ;;
        --garment) garment="${2:?}"; shift 2 ;;
        --skin-base) skin_base="${2:?}"; shift 2 ;;
        --smoothing) smoothing="${2:?}"; shift 2 ;;
        --crop-spec) crop_spec="${2:?}"; shift 2 ;;
        --crop-anchor) crop_anchor="${2:?}"; shift 2 ;;
        --crop-rect) crop_rect="${2:?}"; shift 2 ;;
        --rotation) rotation="${2:?}"; shift 2 ;;
        *) usage ;;
      esac
    done
    mkdir -p "$work"
    state="$work/headshots.json"
    project_response="$(mktemp)" inspect_response="$(mktemp)" preview_request="$(mktemp)" preview_response="$(mktemp)"
    trap 'rm -f "$project_response" "$inspect_response" "$preview_request" "$preview_response"' EXIT
    project_args=(-F "image=@$input")
    if [ -n "$scene" ]; then
      project_args+=(-F "entry_source=scene_gallery" -F "scene_id=$scene")
    else
      project_args+=(-F "entry_source=direct_upload")
    fi
    api_json POST "/v1/headshots/projects" "$project_response" "${project_args[@]}"
    state_save "$state" project "$project_response"
    project_id="$(json_value "$project_response" project_id)"
    api_json POST "/v1/headshots/projects/$project_id/inspect" "$inspect_response"
    state_save "$state" inspection "$inspect_response"
    cp "$inspect_response" "$work/source-check.json"
    python3 - "$inspect_response" <<'PY'
import json, pathlib, sys
d = json.loads(pathlib.Path(sys.argv[1]).read_text())
if not d.get("eligible"):
    reasons = ", ".join(d.get("reasons") or []) or "source is not eligible"
    raise SystemExit(f"headshot source is ineligible: {reasons}")
for warning in d.get("warnings") or []:
    print(f"warning: {warning}", file=sys.stderr)
PY
    if [ -n "$garment" ]; then
      garment_response="$(mktemp)"
      printf '{"garment_preference":"%s"}\n' "$garment" > "$garment_response.request"
      api_json POST "/v1/headshots/projects/$project_id/garment-preference" "$garment_response" -H "Content-Type: application/json" --data-binary "@$garment_response.request"
      state_save "$state" project "$garment_response"
      rm -f "$garment_response" "$garment_response.request"
    fi
    python3 - "$preview_request" "$skin_base" "$smoothing" "$crop_spec" "$crop_anchor" "$crop_rect" "$rotation" <<'PY'
import json, pathlib, sys
out, skin, smoothing, spec, anchor, rect, rotation = sys.argv[1:]
d = {"skin_base_id": skin, "smoothing_strength": float(smoothing), "crop_spec_id": spec,
     "crop_anchor": anchor, "crop_rotation": float(rotation)}
if rect:
    values = [float(v) for v in rect.split(",")]
    if len(values) != 4: raise SystemExit("--crop-rect must be X,Y,W,H")
    d.update(dict(zip(("crop_x", "crop_y", "crop_width", "crop_height"), values)))
pathlib.Path(out).write_text(json.dumps(d))
PY
    api_json POST "/v1/headshots/projects/$project_id/previews" "$preview_response" -H "Content-Type: application/json" --data-binary "@$preview_request"
    state_save "$state" preview "$preview_response"
    preview_url="$(json_value "$preview_response" image.url)"
    api_download "$preview_url" "$work/reference-preview.png"
    echo "prepared $work/reference-preview.png  project=$project_id  preview=$(json_value "$preview_response" preview_id)"
    echo "Review the preview, then run: headshots.sh confirm $work"
    ;;

  confirm)
    require_key
    work="${1:?confirm requires a work directory}"
    state="$work/headshots.json"
    project_id="$(state_get "$state" project_id)"
    preview_id="$(state_get "$state" preview_id)"
    request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$request" "$response"' EXIT
    printf '{"preview_id":"%s"}\n' "$preview_id" > "$request"
    api_json POST "/v1/headshots/projects/$project_id/references" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" reference "$response"
    reference_id="$(json_value "$response" reference_id)"
    api_download "/v1/headshots/projects/$project_id/references/$reference_id/image" "$work/reference.png"
    echo "confirmed $work/reference.png  reference=$reference_id"
    ;;

  start-person)
    require_key
    person_id="${1:?start-person requires a person reference id}"
    work="${2:?start-person requires a work directory}"
    shift 2
    scene=""
    while [ "$#" -gt 0 ]; do
      case "$1" in --scene) scene="${2:?}"; shift 2;; *) usage;; esac
    done
    mkdir -p "$work"
    state="$work/headshots.json" request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$request" "$response"' EXIT
    python3 - "$request" "$person_id" "$scene" <<'PY'
import json, pathlib, sys
d={"person_reference_id":sys.argv[2]}
if sys.argv[3]: d["scene_id"]=sys.argv[3]
pathlib.Path(sys.argv[1]).write_text(json.dumps(d))
PY
    api_json POST "/v1/headshots/projects/from-person-reference" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" project "$response"
    state_save "$state" reference "$response"
    project_id="$(json_value "$response" project_id)" reference_id="$(json_value "$response" reference_id)"
    api_download "/v1/headshots/projects/$project_id/references/$reference_id/image" "$work/reference.png"
    echo "started project=$project_id from person=$person_id  reference=$reference_id"
    ;;

  use-person)
    require_key
    work="${1:?use-person requires a work directory}"
    person_id="${2:?use-person requires a person reference id}"
    state="$work/headshots.json" project_id="$(state_get "$state" project_id)"
    request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$request" "$response"' EXIT
    printf '{"person_reference_id":"%s"}\n' "$person_id" > "$request"
    api_json POST "/v1/headshots/projects/$project_id/person-reference" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" project "$response"
    state_save "$state" reference "$response"
    reference_id="$(json_value "$response" reference_id)"
    api_download "/v1/headshots/projects/$project_id/references/$reference_id/image" "$work/reference.png"
    echo "updated project=$project_id  reference=$reference_id"
    ;;

  remove-person)
    require_key
    person_id="${1:?remove-person requires a person reference id}" response="$(mktemp)"
    trap 'rm -f "$response"' EXIT
    api_json DELETE "/v1/headshots/person-references/$person_id" "$response"
    echo "removed person reference $person_id from the library; existing projects are unchanged"
    ;;

  generate)
    require_key
    work="${1:?generate requires a work directory}"
    shift
    state="$work/headshots.json"
    project_id="$(state_get "$state" project_id)" reference_id="$(state_get "$state" reference_id)"
    scene="" batch_size="1" style="" pose="" outfit="" background="" ratio="" framing=""
    hair="" face=""
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --scene) scene="${2:?}"; shift 2 ;;
        --batch-size) batch_size="${2:?}"; shift 2 ;;
        --style) style="${2:?}"; shift 2 ;;
        --pose) pose="${2:?}"; shift 2 ;;
        --outfit) outfit="${2:?}"; shift 2 ;;
        --background) background="${2:?}"; shift 2 ;;
        --ratio) ratio="${2:?}"; shift 2 ;;
        --framing) framing="${2:?}"; shift 2 ;;
        --hair-grooming) hair="${2:?}"; shift 2 ;;
        --face-refinement) face="${2:?}"; shift 2 ;;
        *) usage ;;
      esac
    done
    [ -n "$scene" ] || scene="$(python3 - "$state" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text()); print((d.get('project') or {}).get('scene_id') or 'professional_profile')
PY
)"
    recommendation_request="$(mktemp)" recommendation_response="$(mktemp)" job_request="$(mktemp)" job_response="$(mktemp)"
    trap 'rm -f "$recommendation_request" "$recommendation_response" "$job_request" "$job_response"' EXIT
    python3 - "$recommendation_request" "$project_id" "$reference_id" "$scene" "$style" "$pose" "$outfit" "$background" "$ratio" "$framing" "$hair" "$face" <<'PY'
import json, pathlib, sys
out, project, reference, scene, style, pose, outfit, background, ratio, framing, hair, face = sys.argv[1:]
d={"project_id":project,"reference_id":reference,"scene_id":scene}
for key, value in (("generation_style_id",style),("pose_id",pose),("outfit_id",outfit),("background_id",background),("output_ratio",ratio),("framing",framing)):
    if value: d[key]=value
for key, value in (("hair_grooming_enabled",hair),("face_refinement_enabled",face)):
    if value: d[key]=value.lower() in {"1","true","yes","on"}
pathlib.Path(out).write_text(json.dumps(d))
PY
    api_json POST "/v1/headshots/recommendation" "$recommendation_response" -H "Content-Type: application/json" --data-binary "@$recommendation_request"
    state_save "$state" configuration "$recommendation_response"
    python3 - "$job_request" "$recommendation_response" "$project_id" "$batch_size" <<'PY'
import json, pathlib, sys
config=json.loads(pathlib.Path(sys.argv[2]).read_text())
keys=("reference_id","scene_id","generation_style_id","pose_id","outfit_id","background_id","hair_grooming_enabled","face_refinement_enabled","framing","output_ratio")
d={"project_id":sys.argv[3],"batch_size":int(sys.argv[4])}
d.update({k:config[k] for k in keys if k in config})
pathlib.Path(sys.argv[1]).write_text(json.dumps(d))
PY
    idem="$(python3 -c 'import uuid; print(uuid.uuid4())')"
    api_json POST "/v1/headshots/jobs" "$job_response" -H "Content-Type: application/json" -H "Idempotency-Key: $idem" --data-binary "@$job_request"
    state_save "$state" job "$job_response"
    echo "submitted job=$(json_value "$job_response" job_id) status=$(json_value "$job_response" status)"
    ;;

  status)
    require_key
    work="${1:?status requires a work directory}" state="$work/headshots.json"
    job_id="$(state_get "$state" job_id)" response="$(mktemp)"
    trap 'rm -f "$response"' EXIT
    api_json GET "/v1/headshots/jobs/$job_id" "$response"
    state_save "$state" job "$response"
    python3 - "$response" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text())
failure=d.get('failure_reason') or d.get('error') or ''
print(f"job={d.get('job_id')} status={d.get('status')} failure={failure}")
for c in d.get("candidates",[]): print(f"  {c.get('ordinal')}  {c.get('candidate_id')}  {c.get('status')}")
PY
    ;;

  download)
    require_key
    work="${1:?download requires a work directory}" state="$work/headshots.json"
    job_id="$(state_get "$state" job_id)" response="$(mktemp)"
    trap 'rm -f "$response"' EXIT
    api_json GET "/v1/headshots/jobs/$job_id" "$response"
    state_save "$state" job "$response"
    python3 - "$response" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text())
if d.get("status") not in {"completed", "partially_completed"}:
    raise SystemExit(f"job is {d.get('status')}; candidates are not ready for download")
if d.get("status") == "partially_completed":
    ready=sum(1 for c in d.get("candidates",[]) if c.get("status")=="ready" and c.get("image_url"))
    print(f"warning: job partially completed; downloading {ready} ready candidate(s)", file=sys.stderr)
PY
    while IFS=$'\t' read -r ordinal candidate_id image_url; do
      [ -n "$image_url" ] || continue
      api_download "$image_url" "$work/candidates/$(printf '%02d' "$ordinal")-$candidate_id.png"
      echo "downloaded candidate $ordinal  $candidate_id"
    done < <(python3 - "$response" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text())
for c in d.get("candidates",[]):
    if c.get("status")=="ready" and c.get("image_url"): print(c.get("ordinal"),c.get("candidate_id"),c.get("image_url"),sep="\t")
PY
)
    ;;

  render)
    require_key
    work="${1:?render requires a work directory}"; shift
    candidate="" style_id="" locale="en"
    while [ "$#" -gt 0 ]; do
      case "$1" in --candidate) candidate="${2:?}"; shift 2;; --style) style_id="${2:?}"; shift 2;; --locale) locale="${2:?}"; shift 2;; *) usage;; esac
    done
    [ -n "$candidate" ] && [ -n "$style_id" ] || usage
    state="$work/headshots.json" candidate_id="$(resolve_candidate "$state" "$candidate")" reference_id="$(state_get "$state" reference_id)"
    styles="$(mktemp)" request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$styles" "$request" "$response"' EXIT
    api_json GET "/v1/headshots/postprocess/styles?reference_id=$reference_id&locale=$locale" "$styles"
    python3 - "$styles" "$style_id" "$request" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text()); wanted=sys.argv[2]
item=next((x for x in d.get("styles",[]) if x.get("id")==wanted),None)
if not item: raise SystemExit(f"unknown postprocess style: {wanted}")
pathlib.Path(sys.argv[3]).write_text(json.dumps({"base_id":item.get("base_id"),"flavour_id":item.get("flavour_id")}))
PY
    api_json POST "/v1/headshots/candidates/$candidate_id/renders" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" render "$response"
    render_id="$(json_value "$response" render_id)"
    api_download "/v1/headshots/renders/$render_id/image" "$work/renders/$render_id.png"
    echo "rendered $work/renders/$render_id.png"
    ;;

  light)
    require_key
    work="${1:?light requires a work directory}"; shift
    candidate="" style_id="natural_dimension" strength="" use_render="false"
    while [ "$#" -gt 0 ]; do
      case "$1" in --candidate) candidate="${2:?}"; shift 2;; --style) style_id="${2:?}"; shift 2;; --strength) strength="${2:?}"; shift 2;; --render) use_render="true"; shift;; *) usage;; esac
    done
    [ -n "$candidate" ] || usage
    state="$work/headshots.json" candidate_id="$(resolve_candidate "$state" "$candidate")"
    source_render_id=""
    [ "$use_render" = "false" ] || source_render_id="$(state_get "$state" render_id)"
    request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$request" "$response"' EXIT
    python3 - "$request" "$style_id" "$strength" "$source_render_id" <<'PY'
import json, pathlib, sys
d={"render_kind":"portrait_lighting","lighting_style":sys.argv[2]}
if sys.argv[3]: d["lighting_strength"]=float(sys.argv[3])
if sys.argv[4]: d["source_render_id"]=sys.argv[4]
pathlib.Path(sys.argv[1]).write_text(json.dumps(d))
PY
    api_json POST "/v1/headshots/candidates/$candidate_id/renders" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" render "$response"
    render_id="$(json_value "$response" render_id)"
    api_download "/v1/headshots/renders/$render_id/image" "$work/renders/$render_id.png"
    echo "light sculpted $work/renders/$render_id.png"
    ;;

  export)
    require_key
    work="${1:?export requires a work directory}"; shift
    candidate="" use_render="false" crop="profile_4x5" format="jpeg" quality="92"
    while [ "$#" -gt 0 ]; do
      case "$1" in --candidate) candidate="${2:?}"; shift 2;; --render) use_render="true"; shift;; --crop) crop="${2:?}"; shift 2;; --format) format="${2:?}"; shift 2;; --quality) quality="${2:?}"; shift 2;; *) usage;; esac
    done
    [ -n "$candidate" ] || usage
    state="$work/headshots.json" candidate_id="$(resolve_candidate "$state" "$candidate")"
    request="$(mktemp)" response="$(mktemp)"
    trap 'rm -f "$request" "$response"' EXIT
    render_id=""
    [ "$use_render" = "false" ] || render_id="$(state_get "$state" render_id)"
    python3 - "$request" "$crop" "$format" "$quality" "$render_id" <<'PY'
import json, pathlib, sys
d={"source_type":"render" if sys.argv[5] else "master","crop_spec_id":sys.argv[2],"format":sys.argv[3],"quality":int(sys.argv[4])}
if sys.argv[5]: d["render_id"]=sys.argv[5]
pathlib.Path(sys.argv[1]).write_text(json.dumps(d))
PY
    api_json POST "/v1/headshots/candidates/$candidate_id/exports" "$response" -H "Content-Type: application/json" --data-binary "@$request"
    state_save "$state" export "$response"
    export_id="$(json_value "$response" export_id)" download_url="$(json_value "$response" download_url)"
    extension="$format"; [ "$extension" != "jpeg" ] || extension="jpg"
    api_download "$download_url" "$work/exports/$export_id.$extension"
    echo "exported $work/exports/$export_id.$extension"
    ;;

  *) usage ;;
esac
