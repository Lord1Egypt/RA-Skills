#!/usr/bin/env python3
"""
OpenLens - Multi-Modal AI Creation Platform
Version: 1.0.5
Features: T2I, T2V, I2V, V2V with Robust API Networking
"""

import streamlit as st
import requests
import json
import time
import base64
from datetime import datetime

# ============================================================
# Translation Dictionary
# ============================================================
TRANSLATIONS = {
    "en": {
        "age_title": "OpenLens", "age_subtitle": "Age Verification Required",
        "age_description": "This platform provides multi-modal AI. By proceeding, you confirm:",
        "age_check_1": "I am 18 years or older", "age_check_2": "I will use legally",
        "age_check_3": "I accept full responsibility", "age_warning": "Illegal content prohibited",
        "age_enter": "I am 18+ - Enter", "age_exit": "Exit", "age_redirecting": "Redirecting...",
        "main_title": "OpenLens", "main_subtitle": "Multi-Modal AI | T2I T2V I2V V2V",
        "config_title": "Configuration", "global_settings": "Global Settings",
        "global_api_url": "API Base URL", "global_api_url_placeholder": "https://api.openai.com/v1",
        "text_model": "Text Model (Prompt)", "text_api_key": "Text API Key", "text_api_key_placeholder": "sk-...",
        "text_model_name": "Model Name", "text_model_placeholder": "gpt-4o",
        "t2i_model": "Image (T2I)", "t2i_api_key": "T2I API Key", "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I Model", "t2i_model_placeholder": "dall-e-3",
        "t2v_model": "Video (T2V)", "t2v_api_key": "T2V API Key", "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V Model", "t2v_model_placeholder": "wan2.2",
        "i2v_model": "I2V", "i2v_api_key": "I2V API Key", "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V Model", "i2v_model_placeholder": "wan2.2",
        "v2v_model": "V2V", "v2v_api_key": "V2V API Key", "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V Model", "v2v_model_placeholder": "wan2.2",
        "save_config": "Save", "save_config_success": "Saved",
        "create_title": "Creation", "step_1": "Select Mode",
        "mode_t2i": "Text-to-Image", "mode_t2v": "Text-to-Video",
        "mode_i2v": "Image-to-Video", "mode_v2v": "Video-to-Video",
        "step_2": "Enter Prompt", "prompt_label": "Describe what you want",
        "prompt_placeholder": "E.g., A cat in sunlight...",
        "use_ai_optimize": "Optimize prompt",
        "step_3": "Media Input", "upload_image": "Upload Image",
        "or_image_url": "Or Image URL", "image_url_placeholder": "https://...",
        "upload_video": "Upload Video", "or_video_url": "Or Video URL",
        "generate": "Generate", "generating": "Generating (1-3 min for video)...",
        "error_no_prompt": "Enter prompt", "error_text_api": "Fill Text API config",
        "error_t2i_api": "Fill T2I API config", "error_t2v_api": "Fill T2V API config",
        "error_i2v_api": "Fill I2V API config", "error_i2v_media": "Add image",
        "error_v2v_api": "Fill V2V API config", "error_v2v_media": "Add video",
        "error_api": "API Error", "error_network": "Network Error",
        "optimize_title": "Optimizing...", "optimize_success": "Optimized!",
        "enhanced": "Enhanced:", "result_title": "Result",
        "result_image": "Image", "result_video": "Video",
        "download": "Download Prompt",
        "footer_title": "OpenLens", "footer_disclaimer": "No API Keys stored",
        "language": "Language", "polling": "Checking... ({}/{})",
        "task_id": "Task ID:", "success": "Success!", "failed": "Failed",
    },
    "zh": {
        "age_title": "OpenLens", "age_subtitle": "需要年龄验证",
        "age_description": "本平台提供多模态AI生成服务。继续即表示确认：",
        "age_check_1": "我已满18岁", "age_check_2": "我将合法使用",
        "age_check_3": "我承担全部责任", "age_warning": "禁止违法内容",
        "age_enter": "我已满18岁 - 进入", "age_exit": "离开", "age_redirecting": "跳转中...",
        "main_title": "OpenLens", "main_subtitle": "多模态AI创作 | T2I T2V I2V V2V",
        "config_title": "配置", "global_settings": "全局设置",
        "global_api_url": "API基础URL", "global_api_url_placeholder": "https://api.openai.com/v1",
        "text_model": "文本模型(提示词)", "text_api_key": "文本API Key", "text_api_key_placeholder": "sk-...",
        "text_model_name": "模型名称", "text_model_placeholder": "gpt-4o",
        "t2i_model": "图像(T2I)", "t2i_api_key": "T2I API Key", "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I模型", "t2i_model_placeholder": "dall-e-3",
        "t2v_model": "视频(T2V)", "t2v_api_key": "T2V API Key", "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V模型", "t2v_model_placeholder": "wan2.2",
        "i2v_model": "图生视频(I2V)", "i2v_api_key": "I2V API Key", "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V模型", "i2v_model_placeholder": "wan2.2",
        "v2v_model": "视频生视频(V2V)", "v2v_api_key": "V2V API Key", "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V模型", "v2v_model_placeholder": "wan2.2",
        "save_config": "保存", "save_config_success": "已保存",
        "create_title": "创作", "step_1": "选择模式",
        "mode_t2i": "文生图", "mode_t2v": "文生视频",
        "mode_i2v": "图生视频", "mode_v2v": "视频生视频",
        "step_2": "输入提示词", "prompt_label": "描述你想生成的内容",
        "prompt_placeholder": "例如：阳光下的猫...",
        "use_ai_optimize": "优化提示词",
        "step_3": "媒体输入", "upload_image": "上传图片",
        "or_image_url": "或图片URL", "image_url_placeholder": "https://...",
        "upload_video": "上传视频", "or_video_url": "或视频URL",
        "generate": "生成", "generating": "生成中...(视频需要1-3分钟)",
        "error_no_prompt": "请输入提示词", "error_text_api": "填写文本API配置",
        "error_t2i_api": "填写T2I API配置", "error_t2v_api": "填写T2V API配置",
        "error_i2v_api": "填写I2V API配置", "error_i2v_media": "添加图片",
        "error_v2v_api": "填写V2V API配置", "error_v2v_media": "添加视频",
        "error_api": "API错误", "error_network": "网络错误",
        "optimize_title": "优化中...", "optimize_success": "优化完成！",
        "enhanced": "优化后:", "result_title": "结果",
        "result_image": "图片", "result_video": "视频",
        "download": "下载提示词",
        "footer_title": "OpenLens", "footer_disclaimer": "不存储API Key",
        "language": "语言", "polling": "检查中... ({}/{})",
        "task_id": "任务ID:", "success": "成功！", "failed": "失败",
    },
    "ja": {
        "age_title": "OpenLens", "age_subtitle": "年齢確認",
        "age_description": "このプラットフォームはマルチモーダルAI。続行で以下を確認：",
        "age_check_1": "18歳以上", "age_check_2": "合法的に使用",
        "age_check_3": "全責任を負う", "age_warning": "違法コンテンツ禁止",
        "age_enter": "18歳以上 - 進む", "age_exit": "退出", "age_redirecting": "リダイレクト...",
        "main_title": "OpenLens", "main_subtitle": "マルチモーダルAI | T2I T2V I2V V2V",
        "config_title": "設定", "global_settings": "グローバル設定",
        "global_api_url": "API Base URL", "global_api_url_placeholder": "https://api.openai.com/v1",
        "text_model": "テキストモデル", "text_api_key": "テキストAPI Key", "text_api_key_placeholder": "sk-...",
        "text_model_name": "モデル名", "text_model_placeholder": "gpt-4o",
        "t2i_model": "画像(T2I)", "t2i_api_key": "T2I API Key", "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I モデル", "t2i_model_placeholder": "dall-e-3",
        "t2v_model": "動画(T2V)", "t2v_api_key": "T2V API Key", "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V モデル", "t2v_model_placeholder": "wan2.2",
        "i2v_model": "画像から動画(I2V)", "i2v_api_key": "I2V API Key", "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V モデル", "i2v_model_placeholder": "wan2.2",
        "v2v_model": "動画から動画(V2V)", "v2v_api_key": "V2V API Key", "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V モデル", "v2v_model_placeholder": "wan2.2",
        "save_config": "保存", "save_config_success": "保存済み",
        "create_title": "作成", "step_1": "モード選択",
        "mode_t2i": "画像生成", "mode_t2v": "動画生成",
        "mode_i2v": "画像から動画", "mode_v2v": "動画から動画",
        "step_2": "プロンプト", "prompt_label": "生成内容を描述",
        "prompt_placeholder": "例：陽光下の猫...",
        "use_ai_optimize": "プロンプト最適化",
        "step_3": "メディア入力", "upload_image": "画像アップロード",
        "or_image_url": "または画像URL", "image_url_placeholder": "https://...",
        "upload_video": "動画アップロード", "or_video_url": "または動画URL",
        "generate": "生成", "generating": "生成中...(動画1-3分)",
        "error_no_prompt": "プロンプトを入力", "error_text_api": "テキストAPI設定",
        "error_t2i_api": "T2I API設定", "error_t2v_api": "T2V API設定",
        "error_i2v_api": "I2V API設定", "error_i2v_media": "画像を追加",
        "error_v2v_api": "V2V API設定", "error_v2v_media": "動画を追加",
        "error_api": "APIエラー", "error_network": "ネットワークエラー",
        "optimize_title": "最適化中...", "optimize_success": "最適化完了！",
        "enhanced": "最適化後:", "result_title": "結果",
        "result_image": "画像", "result_video": "動画",
        "download": "プロンプトDL",
        "footer_title": "OpenLens", "footer_disclaimer": "API Key保存なし",
        "language": "言語", "polling": "確認中... ({}/{})",
        "task_id": "タスクID:", "success": "成功！", "failed": "失敗",
    }
}

def t(key):
    lang = st.session_state.get("current_lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ============================================================
# Session State
# ============================================================
if 'age_verified' not in st.session_state:
    st.session_state.age_verified = False
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = "en"

# ============================================================
# Age Verification
# ============================================================
if not st.session_state.age_verified:
    st.set_page_config(page_title="OpenLens", page_icon="🎬", layout="centered")
    st.markdown("<style>.stApp{background:#0a0a0a}.age-box{background:#1a1a1a;border:2px solid #667eea;border-radius:20px;padding:40px;max-width:500px;margin:80px auto;text-align:center}.age-title{font-size:28px;font-weight:bold;color:#fff;margin-bottom:20px}.age-check{color:#fff;margin:15px 0;text-align:left;padding:0 30px}.stButton>button{width:100%;margin:5px 0}</style>", unsafe_allow_html=True)
    st.markdown(f"<div class='age-box'><div class='age-title'>🎬 {t('age_title')}</div><div style='color:#aaa;margin-bottom:15px'>{t('age_subtitle')}</div><div class='age-check'>✅ {t('age_check_1')}<br>✅ {t('age_check_2')}<br>✅ {t('age_check_3')}</div><div style='color:#ef4444;font-size:12px;margin-top:15px'>{t('age_warning')}</div></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        if st.button(t("age_enter"), type="primary", key="age_enter_btn"):
            st.session_state.age_verified = True
            st.rerun()
    with col2:
        if st.button(t("age_exit"), key="age_exit_btn"):
            st.markdown("<script>window.parent.location.href='https://www.google.com';</script>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# Main Config
# ============================================================
st.set_page_config(page_title="OpenLens", page_icon="🎬", layout="wide")

defaults = {
    "global_api_url": "https://api.openai.com/v1",
    "text_api_key": "", "text_model": "gpt-4o",
    "t2i_api_key": "", "t2i_model": "dall-e-3",
    "t2v_api_key": "", "t2v_model": "wan2.2",
    "i2v_api_key": "", "i2v_model": "wan2.2",
    "v2v_api_key": "", "v2v_model": "wan2.2",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("<style>.stApp{background:#0a0a0a;color:#e0e0e0}.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#1a1a1a;border:1px solid #333;color:#fff}.stButton>button{background:linear-gradient(135deg,#667eea,#764ba2);border:none;color:white}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    lang = st.selectbox(t("language"), ["en","zh","ja"], format_func=lambda x: {"en":"English","zh":"简体中文","ja":"日本語"}[x], index=["en","zh","ja"].index(st.session_state.current_lang))
    if lang != st.session_state.current_lang:
        st.session_state.current_lang = lang
        st.rerun()

# ============================================================
# ROBUST API FUNCTIONS
# ============================================================

def make_headers(api_key):
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def handle_error(resp, msg=""):
    try:
        err = resp.json().get("error", {}).get("message", str(resp.text[:100]))
    except:
        err = resp.text[:100]
    st.error(f"{t('error_api')}: {err} {msg}")
    return None

def call_text(prompt, api_key, model, api_url):
    """文本模型 API"""
    headers = make_headers(api_key)
    payload = {"model": model, "messages":[{"role":"system","content":"Enhance prompt with cinematic details."},{"role":"user","content":prompt}], "temperature":0.7}
    try:
        r = requests.post(f"{api_url}/chat/completions", headers=headers, json=payload, timeout=60)
        if r.status_code != 200: return handle_error(r)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"{t('error_network')}: {e}")
        return None

def call_t2i(prompt, api_key, model, api_url):
    """文生图 API"""
    headers = make_headers(api_key)
    payload = {"model": model, "prompt": prompt, "n":1, "size":"1024x1024"}
    try:
        r = requests.post(f"{api_url}/images/generations", headers=headers, json=payload, timeout=120)
        if r.status_code != 200: return handle_error(r)
        return {"url": r.json()["data"][0]["url"], "type": "image", "prompt": prompt}
    except Exception as e:
        st.error(f"{t('error_network')}: {e}")
        return None

def submit_task(api_url, api_key, payload, endpoint="/video/generations"):
    """提交异步任务"""
    headers = make_headers(api_key)
    try:
        r = requests.post(f"{api_url}{endpoint}", headers=headers, json=payload, timeout=60)
        if r.status_code != 200: return handle_error(r), None
        data = r.json()
        return data.get("task_id") or data.get("id"), data
    except Exception as e:
        st.error(f"{t('error_network')}: {e}")
        return None, None

def poll_status(api_url, api_key, task_id, max_att=72, interval=5):
    """轮询任务状态 - 视频生成核心"""
    headers = make_headers(api_key)
    status = st.empty()
    
    for i in range(1, max_att+1):
        status.info(t("polling").format(i, max_att))
        try:
            for suf in [f"/tasks/{task_id}", f"/video/generations/{task_id}"]:
                try:
                    r = requests.get(f"{api_url}{suf}", headers=headers, timeout=30)
                    if r.status_code == 200: break
                except: continue
            else: continue
            
            data = r.json()
            s = str(data.get("status", data.get("state", ""))).upper()
            
            if s in ["SUCCEED", "SUCCESS", "COMPLETED", "DONE"]:
                for k in ["video_url","output_url","url","video"]:
                    if k in data:
                        status.success(t("success"))
                        return data[k]
                if data.get("videos"):
                    status.success(t("success"))
                    return data["videos"][0].get("video_url", data["videos"][0].get("url"))
            
            if s in ["FAILED","ERROR"]:
                st.error(t("failed") + ": " + str(data.get("error","")))
                return None
            
            time.sleep(interval)
        except Exception as e:
            if i <= 3: time.sleep(interval); continue
            st.error(f"{t('error_network')}: {e}")
            return None
    
    st.error("Timeout")
    return None

def call_t2v(prompt, api_key, model, api_url):
    """文生视频"""
    payload = {"model": model, "input": {"prompt": prompt}, "parameters": {"size":"720p","duration":5}}
    task_id, _ = submit_task(api_url, api_key, payload)
    if not task_id: return None
    st.info(f"{t('task_id')} {task_id}")
    with st.spinner(t("generating")):
        url = poll_status(api_url, api_key, task_id)
    if url: return {"url": url, "type": "video", "prompt": prompt}
    return None

def call_i2v(prompt, img_data, api_key, model, api_url):
    """图生视频"""
    if img_data.startswith("http"):
        payload = {"model": model, "input": {"prompt": prompt, "img_url": img_data}, "parameters": {"size":"720p","duration":5}}
    else:
        payload = {"model": model, "input": {"prompt": prompt, "img_base64": img_data}, "parameters": {"size":"720p","duration":5}}
    task_id, _ = submit_task(api_url, api_key, payload)
    if not task_id: return None
    st.info(f"{t('task_id')} {task_id}")
    with st.spinner(t("generating")):
        url = poll_status(api_url, api_key, task_id)
    if url: return {"url": url, "type": "video", "prompt": prompt}
    return None

def call_v2v(prompt, vid_data, api_key, model, api_url):
    """视频生视频"""
    if vid_data.startswith("http"):
        payload = {"model": model, "input": {"prompt": prompt, "video_url": vid_data}, "parameters": {"size":"720p","duration":5}}
    else:
        payload = {"model": model, "input": {"prompt": prompt, "video_base64": vid_data}, "parameters": {"size":"720p","duration":5}}
    task_id, _ = submit_task(api_url, api_key, payload)
    if not task_id: return None
    st.info(f"{t('task_id')} {task_id}")
    with st.spinner(t("generating")):
        url = poll_status(api_url, api_key, task_id)
    if url: return {"url": url, "type": "video", "prompt": prompt}
    return None

# ============================================================
# Main UI
# ============================================================
st.markdown(f"## 🎬 {t('main_title')} | {t('main_subtitle')}")
st.markdown("---")

c1, c2 = st.columns([1, 2])

with c1:
    st.header(t("config_title"))
    st.session_state.global_api_url = st.text_input(
        t("global_api_url"), 
        st.session_state.global_api_url, 
        placeholder="https://...", 
        key="global_api_url_input",
        label_visibility="visible"
    )
    
    # 文本模型配置
    with st.expander(t("text_model")):
        st.session_state.text_api_key = st.text_input(
            "Text API Key", 
            type="password", 
            placeholder="sk-...",
            key="text_api_key_input",
            label_visibility="visible"
        )
        st.session_state.text_model = st.text_input(
            "Text Model Name", 
            placeholder="gpt-4o",
            key="text_model_input",
            label_visibility="visible"
        )
    
    # T2I 配置
    with st.expander(t("t2i_model")):
        st.session_state.t2i_api_key = st.text_input(
            "T2I API Key", 
            type="password", 
            placeholder="sk-...",
            key="t2i_api_key_input",
            label_visibility="visible"
        )
        st.session_state.t2i_model = st.text_input(
            "T2I Model Name", 
            placeholder="dall-e-3",
            key="t2i_model_input",
            label_visibility="visible"
        )
    
    # T2V 配置
    with st.expander(t("t2v_model")):
        st.session_state.t2v_api_key = st.text_input(
            "T2V API Key", 
            type="password", 
            placeholder="sk-...",
            key="t2v_api_key_input",
            label_visibility="visible"
        )
        st.session_state.t2v_model = st.text_input(
            "T2V Model Name", 
            placeholder="wan2.2",
            key="t2v_model_input",
            label_visibility="visible"
        )
    
    # I2V 配置
    with st.expander(t("i2v_model")):
        st.session_state.i2v_api_key = st.text_input(
            "I2V API Key", 
            type="password", 
            placeholder="sk-...",
            key="i2v_api_key_input",
            label_visibility="visible"
        )
        st.session_state.i2v_model = st.text_input(
            "I2V Model Name", 
            placeholder="wan2.2",
            key="i2v_model_input",
            label_visibility="visible"
        )
    
    # V2V 配置
    with st.expander(t("v2v_model")):
        st.session_state.v2v_api_key = st.text_input(
            "V2V API Key", 
            type="password", 
            placeholder="sk-...",
            key="v2v_api_key_input",
            label_visibility="visible"
        )
        st.session_state.v2v_model = st.text_input(
            "V2V Model Name", 
            placeholder="wan2.2",
            key="v2v_model_input",
            label_visibility="visible"
        )
    
    if st.button(t("save_config"), key="save_config_btn"): 
        st.success(t("save_config_success"))

with c2:
    st.header(t("create_title"))
    st.subheader(t("step_1"))
    mode = st.radio(
        "Mode", 
        ["Text-to-Image","Text-to-Video","Image-to-Video","Video-to-Video"], 
        horizontal=True, 
        label_visibility="collapsed",
        key="mode_radio",
        format_func=lambda x: {"Text-to-Image":t("mode_t2i"),"Text-to-Video":t("mode_t2v"),"Image-to-Video":t("mode_i2v"),"Video-to-Video":t("mode_v2v")}[x]
    )
    
    st.subheader(t("step_2"))
    prompt = st.text_area(t("prompt_label"), height=100, placeholder=t("prompt_placeholder"), key="prompt_input")
    
    use_opt = st.checkbox(t("use_ai_optimize"), key="optimize_checkbox")
    
    media, media_url = None, ""
    st.subheader(t("step_3"))
    if mode == "Image-to-Video":
        media = st.file_uploader(t("upload_image"), type=['jpg','png'], key="image_uploader")
        media_url = st.text_input(t("or_image_url"), placeholder="https://...", key="image_url_input")
        if media: media = base64.b64encode(media.read()).decode()
    elif mode == "Video-to-Video":
        media = st.file_uploader(t("upload_video"), type=['mp4'], key="video_uploader")
        media_url = st.text_input(t("or_video_url"), placeholder="https://...", key="video_url_input")
        if media: media = base64.b64encode(media.read()).decode()
    
    st.markdown("---")
    if st.button(t("generate"), type="primary", use_container_width=True, key="generate_btn"):
        if not prompt: st.error(t("error_no_prompt")); st.stop()
        
        fp = prompt
        if use_opt:
            if not st.session_state.text_api_key or not st.session_state.text_model: st.error(t("error_text_api")); st.stop()
            with st.spinner(t("optimize_title")): fp = call_text(prompt, st.session_state.text_api_key, st.session_state.text_model, st.session_state.global_api_url)
            if fp: st.success(t("optimize_success")); st.info(f"{t('enhanced')} {fp}")
            else: st.stop()
        
        cfg = {
            "Text-to-Image": ("t2i", st.session_state.t2i_api_key, st.session_state.t2i_model, call_t2i),
            "Text-to-Video": ("t2v", st.session_state.t2v_api_key, st.session_state.t2v_model, call_t2v),
            "Image-to-Video": ("i2v", st.session_state.i2v_api_key, st.session_state.i2v_model, call_i2v, media or media_url),
            "Video-to-Video": ("v2v", st.session_state.v2v_api_key, st.session_state.v2v_model, call_v2v, media or media_url),
        }
        
        p = cfg[mode]
        if not p[1] or not p[2]:
            st.error(t(f"error_{p[0]}_api")); st.stop()
        if mode in ["Image-to-Video","Video-to-Video"] and not p[4]:
            st.error(t(f"error_{p[0]}_media")); st.stop()
        
        with st.spinner(t("generating")):
            if mode == "Text-to-Image": result = p[3](fp, p[1], p[2], st.session_state.global_api_url)
            elif mode == "Text-to-Video": result = p[3](fp, p[1], p[2], st.session_state.global_api_url)
            else: result = p[3](fp, p[4], p[1], p[2], st.session_state.global_api_url)
        
        if result:
            st.markdown("---")
            st.subheader(t("result_title"))
            if result["type"]=="image": st.image(result["url"])
            else: st.video(result["url"])
            d = json.dumps({"prompt":result.get("prompt",fp),"mode":mode,"time":datetime.now().isoformat()}, ensure_ascii=False)
            st.download_button(t("download"), d, "prompt.json", "application/json")

st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#666;font-size:12px'>{t('footer_title')} | {t('footer_disclaimer')}</div>", unsafe_allow_html=True)
