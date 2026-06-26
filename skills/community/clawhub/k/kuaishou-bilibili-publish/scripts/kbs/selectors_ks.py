"""快手创作者平台 (cp.kuaishou.com) — CSS / 文案探测用选择器与关键词。

页面结构会变更，若自动化失败请按实际 DOM 更新本文件。

2026-04-03 更新：
- 添加作品描述框选择器
- 添加封面设置相关选择器
- 添加上传按钮选择器
"""

from __future__ import annotations

# 上传页（可能在子路由，脚本会先打开首页再尝试进入视频发布）
HOME_URL = "https://cp.kuaishou.com/"
# 常见视频发布路径（多选一，脚本内会依次尝试）
PUBLISH_VIDEO_URL_CANDIDATES: tuple[str, ...] = (
    "https://cp.kuaishou.com/article/publish/video",
    "https://cp.kuaishou.com/publish/video",
)

# ============ 视频上传 ============
# 主上传区 - 2026-04-03 实测
# 点击"上传视频"按钮触发文件选择（使用通用按钮选择器，具体查找在代码中用 JS）
VIDEO_UPLOAD_BUTTON = 'button.ant-btn, button[class*="upload"]'
# 实际的文件输入（隐藏，由按钮触发）
VIDEO_FILE_INPUT = 'input[type="file"][accept*="video"]'

# ============ 作品描述 ============
# 作品描述文本框 - 标题和关键词都写在这里 (contenteditable div)
# 2026-04-03 实测：id="work-description-edit", class="_description_17g9x_24"
DESCRIPTION_TEXTAREA = '#work-description-edit, div._description_17g9x_24, div[contenteditable="true"][placeholder*="作品描述"]'

# ============ 封面设置 ============
# 封面设置区域 - 2026-04-03 实测
# 封面编辑器容器 class="_high-cover-editor_ps02t_1"
# 封面设置按钮/标签 class="_high-cover-editor-label_ps02t_8"
COVER_SETTING_BUTTON = '._high-cover-editor_ps02t_1, ._high-cover-editor-label_ps02t_8, [class*="cover-editor"], [class*="cover-setting"]'
# 封面文件输入 (隐藏在封面编辑器容器内)
# accept="image/apng,image/bmp,image/ico,image/cur,image/jpg,image/jpeg,image/jfif,image/pjpeg,image/pjp,image/png,image/webp"
COVER_FILE_INPUT = '._high-cover-editor_ps02t_1 input[type="file"][accept*="image"], input[type="file"][accept*="image/apng"]'
# 封面弹窗中的「上传封面」标签 (备用)
COVER_UPLOAD_TAB = '[class*="upload"], [class*="cover-tab"]'
# 上传图片按钮（弹窗内，备用）
COVER_UPLOAD_BUTTON = 'button.ant-btn-primary, button[class*="upload"]'
# 确认按钮（弹窗底部，备用）
COVER_CONFIRM_BUTTON = 'button:contains("确认"), button.ant-btn-primary'

# ============ 发布按钮 ============
# 发布按钮（具体点击逻辑在 publish_kuaishou 中用文案匹配补充）
PUBLISH_BUTTON_CANDIDATES: tuple[str, ...] = (
    "button.publish-btn",
    'button[class*="publish"]',
    'button.ant-btn-primary',
)

# ============ 上传完成 / 失败 文案探测 ============
# 上传完成 / 可编辑 文案探测（document.body.innerText）
TEXT_VIDEO_READY_HINTS: tuple[str, ...] = (
    "上传成功",
    "上传完成",
    "视频已上传",
    "填写信息",
    "视频详情",
    "下一步",
    "编辑封面",
    "编辑标题",
    "拖拽封面",
    "作品描述",
    "封面设置",
)
TEXT_UPLOAD_FAIL_HINTS: tuple[str, ...] = (
    "上传失败", 
    "格式不支持", 
    "文件过大",
    "上传异常",
    "请重新上传"
)
