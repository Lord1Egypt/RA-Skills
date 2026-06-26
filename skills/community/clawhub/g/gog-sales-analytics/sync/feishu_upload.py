import requests
import os
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_DRIVE_FOLDER_ID = os.getenv("FEISHU_DRIVE_FOLDER_ID")

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get tenant_access_token: {data}")
    return data["tenant_access_token"]

def upload_file_to_feishu(file_path, parent_folder_id):
    """Upload a file to Feishu Drive using the multipart upload_all API.

    The upload_all endpoint requires multipart/form-data: metadata fields go in
    the form body (not the query string), and the binary goes through `files`.
    """
    access_token = get_tenant_access_token()
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    form_data = {
        "file_name": file_name,
        "parent_type": "explorer",
        "parent_node": parent_folder_id,
        "size": str(file_size),
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (file_name, f, "application/octet-stream"),
        }
        # Let requests build the multipart body + boundary; do NOT set
        # Content-Type manually or the boundary will be missing.
        response = requests.post(url, headers=headers, data=form_data, files=files)

    try:
        body = response.json()
    except ValueError:
        raise Exception(f"Upload failed (non-JSON response, HTTP {response.status_code}): {response.text}")

    if response.status_code == 200 and body.get("code") == 0:
        file_token = body["data"]["file_token"]
        return f"https://feishu.cn/file/{file_token}"
    else:
        raise Exception(f"Upload failed: {body}")

def set_file_permissions(file_token, permission_type="view", users=None):
    access_token = get_tenant_access_token()
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{file_token}/members?type=file"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    if not users:
        users = ["open_id of team members"]
    
    for user in users:
        payload = {
            "member_type": "openid",
            "member_id": user,
            "perm": permission_type,
            "notify": True
        }
        requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        file_url = upload_file_to_feishu(file_path, FEISHU_DRIVE_FOLDER_ID)
        print(f"File uploaded to Feishu Drive: {file_url}")
