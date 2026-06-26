import argparse
import os
import time
from typing import Any, Dict, Tuple, List
import hashlib
import json
import requests


PI_PPT_BASE_URL = os.getenv("PIPPT_BASE_URL", "")
PI_PPT_APP_ID = os.getenv("PIPPT_APP_ID", "")
PI_PPT_APP_SECRET = os.getenv("PIPPT_APP_SECRET", "")

if not PI_PPT_BASE_URL or not PI_PPT_APP_ID or not PI_PPT_APP_SECRET:
    raise ValueError("PIPPT_BASE_URL, PIPPT_APP_ID and PIPPT_APP_SECRET must be set in the environment. You can obtain API key from the PI website: https://www.pi.inc/ ")

GENERATION_URL = f"{PI_PPT_BASE_URL}/api/v1/integration/document/generation"
GET_STATUS_URL = f"{PI_PPT_BASE_URL}/api/v1/integration/document/status"
UPLOAD_FILE_URL = f"{PI_PPT_BASE_URL}/api/v1/integration/file/upload"

def generate_signature_payload(app_id: str, app_secret: str, **payload: dict) -> Tuple[str, dict]:
    """
    Generate a signed request payload based on timestamp and input parameters.

    Args:
        timestamp: Request timestamp.
        parameters: Key-value parameters that should be included in the signature.

    Returns:
        Request payload with signature fields.
    """

    timestamp = int(time.time())

    # Sort request parameter keys alphabetically.
    keys: List[str] = sorted(payload.keys())

    # Convert non-empty parameters into "key=value" format in sorted order.
    formatted_params: List[str] = []
    for key in keys:
        value = payload[key]
        if isinstance(value, bool):
            formatted_params.append(f"{key}={str(value).lower()}")
        elif isinstance(value, dict):
            formatted_params.append(f"{key}={json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)}")
        elif value is not None:
            formatted_params.append(f"{key}={str(value)}")

    # Join all parameters with colons.
    params_string: str = ":".join(formatted_params)

    # Build signature base string: app_secret:timestamp:params:app_secret
    signature_base = f"{app_secret}:{timestamp}:{params_string}:{app_secret}"

    # Compute SHA1 hash.
    hash_result = hashlib.sha1(signature_base.encode("utf-8")).hexdigest()

    return {"app_id": app_id, "timestamp": timestamp, "sign": hash_result, **payload}


def upload_file(app_id: str, app_secret: str, file_path: str) -> Dict[str, Any]:
    """
    Upload a local file.
    The API requires "file" to be sent as a multipart file field (FILE), not in JSON body.
    Signature fields (app_id, timestamp, sign, name, etc.) are sent in form data
    together with files["file"].
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    file_name = os.path.basename(file_path)
    payload = {"name": file_name}
    payload_with_sign = generate_signature_payload(app_id, app_secret, **payload)

    # In multipart/form-data, serializable fields go to data,
    # while binary content goes to files (field name is usually "file").
    data: Dict[str, str] = {}
    for k, v in payload_with_sign.items():
        if isinstance(v, bool):
            data[k] = str(v).lower()
        elif isinstance(v, (dict, list)):
            data[k] = json.dumps(v, ensure_ascii=False, separators=(",", ":"))
        else:
            data[k] = str(v)

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f)}
        response = requests.post(UPLOAD_FILE_URL, data=data, files=files, timeout=30)
    if response.status_code != 200:
        print(
            f"[upload_file] request failed, status_code={response.status_code}, response_text={response.text}"
        )
    response.raise_for_status()
    return response.json()

def create_document(app_id: str, app_secret: str, content: str, cards: int = 8, language: str = "zh", attachment_id: str = None) -> Dict[str, Any]:
    """
    Trigger Pi PPT generation task only (no polling).
    """
    if not isinstance(content, str) or not content.strip():
        raise ValueError("content must be a non-empty string.")
    if not isinstance(cards, int) or cards <= 0:
        raise ValueError("cards must be a positive integer.")
    if language not in {"zh", "en"}:
        raise ValueError("language must be one of 'zh', 'en'.")

    resource_id = f"draft-{time.time()}"

    payload = {
        "resource_id": resource_id,
        "uid": "user_1",
        "content": content.strip(),
        "cards": cards,
        "language": language,
        "outline_type": "aippt",
        "export":False,
        "inputs_type": "skill"
    }
    if attachment_id:
        payload["attachment_id"] = attachment_id
    else:
        payload["search"] = True

    payload_with_sign = generate_signature_payload(app_id, app_secret, **payload)

    response = requests.post(GENERATION_URL, json=payload_with_sign, timeout=30)
    if response.status_code != 200:
        print(
            f"[create_document] request failed, status_code={response.status_code}, response_text={response.text}"
        )
    response.raise_for_status()
    data = response.json()

    return {
        "name": "generate_pi_ppt",
        "request": payload_with_sign,
        "response": data,
    }

def get_status(app_id: str, app_secret: str, resource_id: str) -> Dict[str, Any]:
    if not isinstance(resource_id, str) or not resource_id.strip():
        raise ValueError("resource_id must be a non-empty string.")

    timestamp = int(time.time())
    payload = {
        "resource_id": resource_id.strip(),
    }
    payload_with_sign = generate_signature_payload(app_id, app_secret, **payload)
    response = requests.post(GET_STATUS_URL, json=payload_with_sign, timeout=30)
    if response.status_code != 200:
        print(
            f"[get_status] request failed, status_code={response.status_code}, response_text={response.text}"
        )
    response.raise_for_status()
    response_json = response.json()

    return response_json
    #data = response_json.get("data")
    #if not isinstance(data, dict):
    #    raise ValueError(f"Status API returned unexpected format: {response_json}")

    #status = data.get("status")
    #if status not in {"running", "fail", "done"}:
    #    raise ValueError(f"Unknown status value: {status}, raw response: {response_json}")

    #return {
    #    "resource_id": data.get("resource_id"),
    #    "status": status,
    #    "url": data.get("url"),
    #}

def generate_pi_ppt(
    app_id: str,
    app_secret: str,
    content: str,
    cards: int = 8,
    language: str = "zh",
    file_path: str = None,
    timeout_s: int = 500,
    poll_interval_s: int = 15,
) -> Dict[str, Any]:
    """
    Full flow:
    1) If file_path is provided, call upload_file to upload the file.
    2) Call create_document to start generation (do not pass cards for uploaded documents).
    3) Poll with get_status until status is done and URL is returned.
    """

    attachment_id = None
    if file_path:
        print(f"Uploading file: {file_path}")
        upload_result = upload_file(app_id, app_secret, file_path)
        attachment_id = upload_result.get("data", {}).get("id")
        if not attachment_id:
            raise ValueError(f"File upload failed: {upload_result}")
        print(f"File uploaded successfully, attachment_id={attachment_id}")

    create_result = create_document(
        app_id=app_id,
        app_secret=app_secret,
        content=content,
        cards=cards,
        language=language,
        attachment_id=attachment_id,
    )

    resource_id = create_result.get("request", {}).get("resource_id")
    if not isinstance(resource_id, str) or not resource_id:
        raise ValueError(f"Creation API did not return a usable resource_id: {create_result}")

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status_result = get_status(app_id, app_secret, resource_id)
        #print(status_result)
        status = status_result.get("data", {}).get("status", "")
        if status == "done":
            url = ""
            if status_result.get("data", {}).get("document_id", ""):
                url = "{}/docs/{}".format(PI_PPT_BASE_URL, status_result.get("data", {}).get("document_id", ""))
            else:
                url = status_result.get("data", {}).get("url", "")
            
            if not url:
                raise ValueError(f"status is 'done' but no url was returned: {status_result}")
            return {
                "resource_id": resource_id,
                "status": "ppt generation success",
                "url": url,
                "create_result": create_result,
            }
        elif status == "running":
            print(f"PPT generation is running, please wait... resource_id={resource_id}")
        elif status == "fail":
            raise RuntimeError(f"PPT generation failed: {status_result}")

        time.sleep(poll_interval_s)

    raise TimeoutError(
        f"Polling timed out after {timeout_s}s, resource_id={resource_id}, status={status}"
    )

def parse_args():
    SUPPORTED_EXTS = {".doc", ".docx", ".txt", ".md", ".pdf", ".pptx", ".ppt"}
    parser = argparse.ArgumentParser(description="Generate PPT using the PI service.")
    parser.add_argument("--content", required=True, help="Topic and description, for example: 'Create a business-style PPT introducing Chinese GPU vendors'.")
    parser.add_argument("--language", default="zh", choices=["zh", "en"], help="PPT language. 'zh' for Chinese, 'en' for English. Default is 'zh'.")
    parser.add_argument("--cards", type=int, default=8, help="Expected number of PPT slides. Default is 8. This argument is ignored when uploading a document.")
    parser.add_argument("--file", default=None, help="Path to the document to upload. Supported formats: .doc/.docx/.txt/.md/.pdf/.pptx/.ppt")
    args = parser.parse_args()

    if args.file:
        ext = os.path.splitext(args.file)[1].lower()
        if ext not in SUPPORTED_EXTS:
            parser.error(
                f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(SUPPORTED_EXTS))}"
            )

    return args


def main():
    args = parse_args()
    pippt_app_id = os.getenv("PIPPT_APP_ID", "").strip()
    pippt_app_secret = os.getenv("PIPPT_APP_SECRET", "").strip()
    if not pippt_app_id or not pippt_app_secret:
        raise ValueError("PIPPT_BASE_URL, PIPPT_APP_ID and PIPPT_APP_SECRET must be set in the environment. You can obtain API key from the PI website: https://www.pi.inc/ ")
    print("Starting PPT generation; this usually takes about 3-6 minutes, please wait...")
    result = generate_pi_ppt(
        app_id=pippt_app_id,
        app_secret=pippt_app_secret,
        content=args.content,
        cards=args.cards,
        language=args.language,
        file_path=args.file,
    )
    url = result.get("url")
    if not url:
        raise ValueError(f"Generation failed: {result}")
    print(f"PPT generated successfully. Click the following link to view/edit/download the ppt: \n{url}")


if __name__ == "__main__":
    main()
