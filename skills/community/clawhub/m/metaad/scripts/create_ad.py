#!/usr/bin/env python3
"""
创建 Meta 广告 (Ad)
包含广告文案、素材、CTA 等
"""

from meta_api import api_post, get_ad_account_id


def create_ad(
    adset_id,
    name,
    creative,
    status="PAUSED",
    tracking_specs=None
):
    """
    创建广告
    
    Args:
        adset_id: 所属广告组 ID
        name: 广告名称
        creative: 广告创意字典
        status: 状态
        tracking_specs: 追踪设置（可选）
    
    Returns:
        dict: 包含 ad_id 的字典
    """
    account_id = get_ad_account_id()
    
    params = {
        "adset_id": adset_id,
        "name": name,
        "creative": creative,
        "status": status,
    }
    
    if tracking_specs:
        params["tracking_specs"] = tracking_specs
    
    result = api_post(f"{account_id}/ads", params)
    
    ad_id = result.get('id')
    print(f"✅ 广告创建成功")
    print(f"   名称: {name}")
    print(f"   ID: {ad_id}")
    
    return {
        "ad_id": ad_id,
        "name": name
    }


def build_creative(
    name,
    page_id,
    message,
    headline=None,
    description=None,
    call_to_action="SHOP_NOW",
    image_hash=None,
    video_id=None,
    link_url=None,
    display_link=None
):
    """
    构建广告创意
    
    Args:
        name: 创意名称
        page_id: Facebook 主页 ID
        message: 广告文案
        headline: 标题
        description: 描述
        call_to_action: CTA 按钮类型
        image_hash: 图片 hash（上传后获得）
        video_id: 视频 ID（上传后获得）
        link_url: 落地页链接
        display_link: 显示的链接
    
    Returns:
        dict: creative 参数
    """
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "message": message,
            "call_to_action": {"type": call_to_action}
        }
    }
    
    # 图片或视频
    if image_hash:
        object_story_spec["link_data"]["image_hash"] = image_hash
    elif video_id:
        object_story_spec["video_data"] = {
            "video_id": video_id,
            "message": message,
            "call_to_action": {"type": call_to_action}
        }
        del object_story_spec["link_data"]
    
    # 链接相关
    if link_url:
        if "link_data" in object_story_spec:
            object_story_spec["link_data"]["link"] = link_url
        if "video_data" in object_story_spec:
            object_story_spec["video_data"]["link"] = link_url
    
    if display_link:
        if "link_data" in object_story_spec:
            object_story_spec["link_data"]["caption"] = display_link
    
    if headline:
        if "link_data" in object_story_spec:
            object_story_spec["link_data"]["name"] = headline
        if "video_data" in object_story_spec:
            object_story_spec["video_data"]["title"] = headline
    
    if description:
        if "link_data" in object_story_spec:
            object_story_spec["link_data"]["description"] = description
    
    creative = {
        "name": name,
        "object_story_spec": object_story_spec
    }
    
    return creative


# CTA 按钮类型
CTA_TYPES = [
    "SHOP_NOW",           # 立即购买
    "LEARN_MORE",         # 了解更多
    "SIGN_UP",            # 注册
    "DOWNLOAD",           # 下载
    "BOOK_TRAVEL",        # 预订行程
    "CONTACT_US",         # 联系我们
    "GET_OFFER",          # 获取优惠
    "GET_QUOTE",          # 获取报价
    "SUBSCRIBE",          # 订阅
    "WATCH_MORE",         # 观看更多
    "SEND_MESSAGE",       # 发送消息
    "APPLY_NOW",          # 立即申请
    "DONATE_NOW",         # 立即捐赠
    "GET_DIRECTIONS",     # 获取路线
    "REQUEST_TIME",       # 预约时间
]


def list_cta_types():
    """列出可用的 CTA 按钮类型"""
    print("=== 可用的 CTA 按钮 ===")
    for cta in CTA_TYPES:
        print(f"  - {cta}")


if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 4:
        print("用法: python create_ad.py <adset_id> <名称> <creative_json>")
        print("\n示例:")
        print('''python create_ad.py 123456789 "我的广告" '{
            "name": "创意1",
            "object_story_spec": {
                "page_id": "YOUR_PAGE_ID",
                "link_data": {
                    "message": "限时优惠！",
                    "image_hash": "IMAGE_HASH",
                    "link": "https://example.com",
                    "call_to_action": {"type": "SHOP_NOW"}
                }
            }
        }' ''')
        print("\n可用的 CTA 按钮:")
        list_cta_types()
        exit(1)
    
    adset_id = sys.argv[1]
    name = sys.argv[2]
    creative = json.loads(sys.argv[3])
    
    print(f"=== 创建广告 ===\n")
    
    try:
        result = create_ad(adset_id, name, creative)
        print(f"\n广告 ID: {result['ad_id']}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
