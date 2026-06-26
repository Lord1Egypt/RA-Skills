"""
OpenLens-Web — Multimodal AI Creation Dashboard
A unified Streamlit interface for T2I, T2V, I2V, and V2V generation.
"""

import time
import io
import requests
import streamlit as st

# ─────────────────────────────────────────────────────────────
# 0.  Page config  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OpenLens-Web",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# 1.  i18n dictionary
# ─────────────────────────────────────────────────────────────
LANG = {
    "English": {
        "title": "🎬 OpenLens-Web",
        "subtitle": "Multimodal AI Creation Dashboard",
        "lang_label": "🌐 Language",
        "gate_title": "🔞 Age Verification Required",
        "gate_body": "This platform provides access to unrestricted AI generation tools.\nYou must be 18 or older to continue.",
        "gate_enter": "✅ I am 18+ — Enter",
        "gate_leave": "❌ Leave",
        "config_title": "⚙️ Configuration",
        "global_section": "🌐 Global Base URL",
        "base_url_label": "Base URL",
        "api_key_label": "API Key",
        "model_id_label": "Model ID",
        "text_section": "💬 Text / Enhance",
        "t2i_section": "🖼️ Text → Image (T2I)",
        "t2v_section": "🎬 Text → Video (T2V)",
        "i2v_section": "🖼️➡️🎬 Image → Video (I2V)",
        "v2v_section": "🎬➡️🎬 Video → Video (V2V)",
        "workspace_title": "🚀 Workspace",
        "task_label": "Task",
        "prompt_label": "Prompt",
        "prompt_placeholder": "Describe what you want to generate…",
        "enhance_label": "✨ Enhance prompt with AI",
        "enhance_btn": "✨ Enhance",
        "enhancing": "Enhancing prompt…",
        "upload_image": "Upload source image",
        "upload_video": "Upload source video",
        "resolution_label": "Resolution",
        "duration_label": "Duration (seconds)",
        "steps_label": "Steps (T2I)",
        "generate_btn": "🚀 Generate",
        "generating_text": "Generating… this may take a moment",
        "polling": "Waiting for video… (task: {})",
        "success_img": "✅ Image generated!",
        "success_vid": "✅ Video generated!",
        "download_img": "⬇️ Download Image",
        "download_vid": "⬇️ Download Video",
        "warn_key": "⚠️ Please fill in the API Key and Model ID for the selected task.",
        "warn_prompt": "⚠️ Please enter a prompt.",
        "warn_upload": "⚠️ Please upload the required source file.",
        "warn_text_key": "⚠️ Text API Key required to enhance prompt.",
        "err_api": "❌ API error: {}",
        "err_timeout": "❌ Task timed out after 5 minutes.",
        "tasks": ["Text → Image (T2I)", "Text → Video (T2V)", "Image → Video (I2V)", "Video → Video (V2V)"],
    },
    "简体中文": {
        "title": "🎬 OpenLens-Web",
        "subtitle": "多模态 AI 创作工作台",
        "lang_label": "🌐 语言",
        "gate_title": "🔞 年龄验证",
        "gate_body": "本平台提供不受限制的 AI 生成工具访问。\n您必须年满 18 岁才能继续。",
        "gate_enter": "✅ 我已满 18 岁 — 进入",
        "gate_leave": "❌ 离开",
        "config_title": "⚙️ 配置",
        "global_section": "🌐 全局 Base URL",
        "base_url_label": "Base URL",
        "api_key_label": "API Key",
        "model_id_label": "Model ID",
        "text_section": "💬 文本 / 提示词增强",
        "t2i_section": "🖼️ 文本 → 图像 (T2I)",
        "t2v_section": "🎬 文本 → 视频 (T2V)",
        "i2v_section": "🖼️➡️🎬 图像 → 视频 (I2V)",
        "v2v_section": "🎬➡️🎬 视频 → 视频 (V2V)",
        "workspace_title": "🚀 工作区",
        "task_label": "任务",
        "prompt_label": "提示词",
        "prompt_placeholder": "描述你想生成的内容…",
        "enhance_label": "✨ AI 增强提示词",
        "enhance_btn": "✨ 增强",
        "enhancing": "正在增强提示词…",
        "upload_image": "上传源图像",
        "upload_video": "上传源视频",
        "resolution_label": "分辨率",
        "duration_label": "时长（秒）",
        "steps_label": "推理步数 (T2I)",
        "generate_btn": "🚀 开始生成",
        "generating_text": "生成中… 请稍候",
        "polling": "等待视频生成… (任务 ID: {})",
        "success_img": "✅ 图像生成成功！",
        "success_vid": "✅ 视频生成成功！",
        "download_img": "⬇️ 下载图像",
        "download_vid": "⬇️ 下载视频",
        "warn_key": "⚠️ 请填写所选任务的 API Key 和 Model ID。",
        "warn_prompt": "⚠️ 请输入提示词。",
        "warn_upload": "⚠️ 请上传所需的源文件。",
        "warn_text_key": "⚠️ 需要填写文本 API Key 才能增强提示词。",
        "err_api": "❌ API 错误：{}",
        "err_timeout": "❌ 任务超时（超过 5 分钟）。",
        "tasks": ["文本 → 图像 (T2I)", "文本 → 视频 (T2V)", "图像 → 视频 (I2V)", "视频 → 视频 (V2V)"],
    },
    "日本語": {
        "title": "🎬 OpenLens-Web",
        "subtitle": "マルチモーダル AI クリエイションダッシュボード",
        "lang_label": "🌐 言語",
        "gate_title": "🔞 年齢確認",
        "gate_body": "このプラットフォームは制限なしの AI 生成ツールへのアクセスを提供します。\n18歳以上の方のみご利用いただけます。",
        "gate_enter": "✅ 18歳以上です — 入場",
        "gate_leave": "❌ 退出",
        "config_title": "⚙️ 設定",
        "global_section": "🌐 グローバル Base URL",
        "base_url_label": "Base URL",
        "api_key_label": "API Key",
        "model_id_label": "Model ID",
        "text_section": "💬 テキスト / 強化",
        "t2i_section": "🖼️ テキスト → 画像 (T2I)",
        "t2v_section": "🎬 テキスト → 動画 (T2V)",
        "i2v_section": "🖼️➡️🎬 画像 → 動画 (I2V)",
        "v2v_section": "🎬➡️🎬 動画 → 動画 (V2V)",
        "workspace_title": "🚀 ワークスペース",
        "task_label": "タスク",
        "prompt_label": "プロンプト",
        "prompt_placeholder": "生成したい内容を説明してください…",
        "enhance_label": "✨ AI でプロンプトを強化",
        "enhance_btn": "✨ 強化",
        "enhancing": "プロンプトを強化中…",
        "upload_image": "ソース画像をアップロード",
        "upload_video": "ソース動画をアップロード",
        "resolution_label": "解像度",
        "duration_label": "長さ（秒）",
        "steps_label": "ステップ数 (T2I)",
        "generate_btn": "🚀 生成開始",
        "generating_text": "生成中… しばらくお待ちください",
        "polling": "動画の生成を待機中… (タスク: {})",
        "success_img": "✅ 画像の生成が完了しました！",
        "success_vid": "✅ 動画の生成が完了しました！",
        "download_img": "⬇️ 画像をダウンロード",
        "download_vid": "⬇️ 動画をダウンロード",
        "warn_key": "⚠️ 選択したタスクの API Key と Model ID を入力してください。",
        "warn_prompt": "⚠️ プロンプトを入力してください。",
        "warn_upload": "⚠️ 必要なソースファイルをアップロードしてください。",
        "warn_text_key": "⚠️ プロンプト強化には テキスト API Key が必要です。",
        "err_api": "❌ API エラー：{}",
        "err_timeout": "❌ タスクが5分でタイムアウトしました。",
        "tasks": ["テキスト → 画像 (T2I)", "テキスト → 動画 (T2V)", "画像 → 動画 (I2V)", "動画 → 動画 (V2V)"],
    },
}

TASK_KEYS = ["T2I", "T2V", "I2V", "V2V"]

# ─────────────────────────────────────────────────────────────
# 2.  Session state initialisation
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "verified": False,
        "lang": "简体中文",
        "result_bytes": None,
        "result_type": None,   # "image" | "video"
        "result_ext": "png",
        "prompt": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────
# 3.  Language selector (always visible in top-right)
# ─────────────────────────────────────────────────────────────
_lang_col, _title_col = st.columns([1, 5])
with _lang_col:
    chosen_lang = st.selectbox(
        label="🌐",
        options=list(LANG.keys()),
        index=list(LANG.keys()).index(st.session_state["lang"]),
        key="lang_selector",
        label_visibility="collapsed",
    )
    if chosen_lang != st.session_state["lang"]:
        st.session_state["lang"] = chosen_lang
        st.rerun()

T = LANG[st.session_state["lang"]]  # active translation dict

with _title_col:
    st.markdown(f"## {T['title']}")
    st.caption(T["subtitle"])

st.divider()

# ─────────────────────────────────────────────────────────────
# 4.  18+ Gate
# ─────────────────────────────────────────────────────────────
if not st.session_state["verified"]:
    st.markdown(f"### {T['gate_title']}")
    st.warning(T["gate_body"])
    col_enter, col_leave, _ = st.columns([1, 1, 4])
    with col_enter:
        if st.button(T["gate_enter"], use_container_width=True):
            st.session_state["verified"] = True
            st.rerun()
    with col_leave:
        # Redirect to google.com on leave
        import streamlit.components.v1 as components
        if st.button(T["gate_leave"], use_container_width=True):
            components.html(
                "<script>window.parent.location.href='https://www.google.com';</script>",
                height=0,
            )
    st.stop()

# ─────────────────────────────────────────────────────────────
# 5.  Helper functions
# ─────────────────────────────────────────────────────────────

def _headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def enhance_prompt(base_url: str, api_key: str, text_model: str, prompt: str) -> str:
    """Call the text model to rewrite the prompt into a detailed generation prompt."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": text_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional AI art director. "
                    "Rewrite the user's short idea into a vivid, detailed generation prompt "
                    "optimized for image/video AI models. Output ONLY the improved prompt, no extra text."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 400,
    }
    resp = requests.post(url, headers=_headers(api_key), json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def generate_image(base_url: str, api_key: str, model: str,
                   prompt: str, resolution: str, steps: int) -> bytes:
    """Call /v1/images/generations and return raw image bytes."""
    w, h = resolution.split("x")
    url = f"{base_url.rstrip('/')}/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "width": int(w),
        "height": int(h),
        "steps": steps,
        "response_format": "url",
    }
    resp = requests.post(url, headers=_headers(api_key), json=payload, timeout=60)
    resp.raise_for_status()
    image_url = resp.json()["data"][0]["url"]
    return requests.get(image_url, timeout=60).content


def submit_video_task(base_url: str, api_key: str, model: str,
                      prompt: str, resolution: str, duration: int,
                      image_bytes: bytes | None = None,
                      video_bytes: bytes | None = None) -> str:
    """Submit a video generation task and return the task_id."""
    url = f"{base_url.rstrip('/')}/video/generations"
    w, h = resolution.split("x")
    payload: dict = {
        "model": model,
        "prompt": prompt,
        "duration": duration,
        "width": int(w),
        "height": int(h),
    }
    files = None
    headers = {"Authorization": f"Bearer {api_key}"}

    if image_bytes:
        # Multipart upload for I2V
        files = {"image": ("source.jpg", image_bytes, "image/jpeg")}
        del payload["model"]  # some APIs separate model via form field
        data = {**payload, "model": model}
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=60)
    elif video_bytes:
        files = {"video": ("source.mp4", video_bytes, "video/mp4")}
        data = {**payload, "model": model}
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=60)
    else:
        resp = requests.post(url, headers=_headers(api_key), json=payload, timeout=60)

    resp.raise_for_status()
    body = resp.json()
    # Support both {id:...} and {task_id:...} response shapes
    return body.get("id") or body.get("task_id") or body["data"]["id"]


def poll_video_task(base_url: str, api_key: str, task_id: str,
                    spinner_text: str, timeout_sec: int = 300) -> bytes:
    """Poll task status until SUCCEED, then download and return video bytes."""
    status_url = f"{base_url.rstrip('/')}/video/generations/{task_id}"
    deadline = time.time() + timeout_sec
    with st.spinner(spinner_text):
        while time.time() < deadline:
            resp = requests.get(status_url, headers=_headers(api_key), timeout=30)
            resp.raise_for_status()
            data = resp.json()
            status = (data.get("status") or data.get("state") or "").upper()
            if status in ("SUCCEED", "SUCCESS", "COMPLETED", "DONE"):
                video_url = (
                    data.get("video_url")
                    or (data.get("videos") or [{}])[0].get("url")
                    or (data.get("videos") or [{}])[0].get("video_url")
                    or data.get("output", {}).get("url")
                )
                return requests.get(video_url, timeout=120).content
            if status in ("FAILED", "ERROR", "CANCELLED"):
                raise RuntimeError(f"Task failed with status: {status}")
            time.sleep(5)
    raise TimeoutError("Task timed out after 5 minutes.")


# ─────────────────────────────────────────────────────────────
# 6.  Main layout — two columns
# ─────────────────────────────────────────────────────────────
col_config, col_workspace = st.columns([1, 2], gap="large")

# ── Left column: Configuration ─────────────────────────────
with col_config:
    st.subheader(T["config_title"])

    # Global Base URL (shared fallback)
    with st.expander(T["global_section"], expanded=True):
        global_base_url = st.text_input(
            T["base_url_label"],
            value="https://api.onlypixai.com/v1",
            key="global_base_url_input",
        )

    # Text / Enhance model
    with st.expander(T["text_section"], expanded=False):
        text_api_key = st.text_input(
            T["api_key_label"], type="password", key="text_api_key_input"
        )
        text_model = st.text_input(
            T["model_id_label"],
            value="pa/grok-4-1-fast-non-reasoning",
            key="text_model_input",
        )

    # Per-task API settings
    # Each task gets its own expander with unique keys
    task_configs: dict[str, dict] = {}

    _task_meta = [
        ("T2I", T["t2i_section"]),
        ("T2V", T["t2v_section"]),
        ("I2V", T["i2v_section"]),
        ("V2V", T["v2v_section"]),
    ]

    for mode, section_label in _task_meta:
        with st.expander(section_label, expanded=False):
            use_global = st.checkbox(
                "Use global Base URL", value=True, key=f"{mode}_use_global_chk"
            )
            task_base_url = (
                global_base_url
                if use_global
                else st.text_input(
                    T["base_url_label"],
                    key=f"{mode}_base_url_input",
                )
            )
            task_api_key = st.text_input(
                T["api_key_label"],
                type="password",
                key=f"{mode}_api_key_input",
            )
            # Sensible default model IDs
            default_models = {
                "T2I": "flux.1-schnell",
                "T2V": "video/wan2.6-t2v",
                "I2V": "video/wan2.6-i2v",
                "V2V": "video/wan2.6-i2v",
            }
            task_model = st.text_input(
                T["model_id_label"],
                value=default_models[mode],
                key=f"{mode}_model_input",
            )
            task_configs[mode] = {
                "base_url": task_base_url,
                "api_key": task_api_key,
                "model": task_model,
            }

    # Generation parameters
    st.divider()
    st.caption("⚙️ Generation Parameters")

    resolution_options_img = ["512x512", "768x768", "1024x1024", "1280x720", "1920x1080"]
    resolution_options_vid = ["1280x720", "1920x1080", "854x480"]

    img_resolution = st.selectbox(
        f"{T['resolution_label']} (T2I)",
        resolution_options_img,
        index=2,
        key="img_resolution_select",
    )
    vid_resolution = st.selectbox(
        f"{T['resolution_label']} (Video)",
        resolution_options_vid,
        index=0,
        key="vid_resolution_select",
    )
    duration = st.selectbox(
        T["duration_label"],
        [5, 10, 15],
        index=0,
        key="duration_select",
    )
    steps = st.slider(
        T["steps_label"],
        min_value=10, max_value=50, value=20, step=5,
        key="steps_slider",
    )

# ── Right column: Workspace ────────────────────────────────
with col_workspace:
    st.subheader(T["workspace_title"])

    # Task selector
    task_display = st.selectbox(
        T["task_label"],
        T["tasks"],
        key="task_selector",
    )
    # Map display name back to key
    task_key = TASK_KEYS[T["tasks"].index(task_display)]

    # Prompt area
    prompt = st.text_area(
        T["prompt_label"],
        placeholder=T["prompt_placeholder"],
        height=130,
        key="prompt_input",
    )

    # Enhance prompt
    do_enhance = st.checkbox(T["enhance_label"], key="enhance_chk")
    if do_enhance:
        if st.button(T["enhance_btn"], key="enhance_btn"):
            if not text_api_key:
                st.warning(T["warn_text_key"])
            elif not prompt:
                st.warning(T["warn_prompt"])
            else:
                with st.spinner(T["enhancing"]):
                    try:
                        enhanced = enhance_prompt(
                            global_base_url, text_api_key, text_model, prompt
                        )
                        st.session_state["prompt"] = enhanced
                        st.success(f"**Enhanced:** {enhanced}")
                    except Exception as e:
                        st.error(T["err_api"].format(e))

    # Dynamic file uploader
    uploaded_image = None
    uploaded_video = None
    if task_key == "I2V":
        uploaded_image = st.file_uploader(
            T["upload_image"],
            type=["jpg", "jpeg", "png", "webp"],
            key="i2v_image_uploader",
        )
    elif task_key == "V2V":
        uploaded_video = st.file_uploader(
            T["upload_video"],
            type=["mp4", "mov", "avi"],
            key="v2v_video_uploader",
        )

    st.divider()

    # ── Generate button ──────────────────────────────────────
    if st.button(T["generate_btn"], type="primary", use_container_width=True, key="generate_btn"):
        cfg = task_configs[task_key]

        # Validation
        if not cfg["api_key"] or not cfg["model"]:
            st.warning(T["warn_key"])
            st.stop()
        if not prompt:
            st.warning(T["warn_prompt"])
            st.stop()
        if task_key == "I2V" and not uploaded_image:
            st.warning(T["warn_upload"])
            st.stop()
        if task_key == "V2V" and not uploaded_video:
            st.warning(T["warn_upload"])
            st.stop()

        # Clear previous result
        st.session_state["result_bytes"] = None
        st.session_state["result_type"] = None

        try:
            if task_key == "T2I":
                # ── Text → Image ─────────────────────────────
                with st.spinner(T["generating_text"]):
                    img_bytes = generate_image(
                        cfg["base_url"], cfg["api_key"], cfg["model"],
                        prompt, img_resolution, steps,
                    )
                st.session_state["result_bytes"] = img_bytes
                st.session_state["result_type"] = "image"
                st.session_state["result_ext"] = "png"

            else:
                # ── Video tasks ──────────────────────────────
                img_bytes_src = uploaded_image.read() if uploaded_image else None
                vid_bytes_src = uploaded_video.read() if uploaded_video else None

                with st.spinner(T["generating_text"]):
                    task_id = submit_video_task(
                        cfg["base_url"], cfg["api_key"], cfg["model"],
                        prompt, vid_resolution, duration,
                        image_bytes=img_bytes_src,
                        video_bytes=vid_bytes_src,
                    )

                vid_bytes = poll_video_task(
                    cfg["base_url"], cfg["api_key"], task_id,
                    T["polling"].format(task_id),
                )
                st.session_state["result_bytes"] = vid_bytes
                st.session_state["result_type"] = "video"
                st.session_state["result_ext"] = "mp4"

        except TimeoutError:
            st.error(T["err_timeout"])
        except Exception as e:
            st.error(T["err_api"].format(e))

    # ── Result display ───────────────────────────────────────
    if st.session_state.get("result_bytes"):
        result_bytes = st.session_state["result_bytes"]
        result_type = st.session_state["result_type"]
        result_ext  = st.session_state["result_ext"]
        filename    = f"openlens_output.{result_ext}"

        if result_type == "image":
            st.success(T["success_img"])
            st.image(result_bytes, use_container_width=True)
            st.download_button(
                label=T["download_img"],
                data=result_bytes,
                file_name=filename,
                mime="image/png",
                key="dl_image_btn",
            )
        elif result_type == "video":
            st.success(T["success_vid"])
            st.video(result_bytes)
            st.download_button(
                label=T["download_vid"],
                data=result_bytes,
                file_name=filename,
                mime="video/mp4",
                key="dl_video_btn",
            )
