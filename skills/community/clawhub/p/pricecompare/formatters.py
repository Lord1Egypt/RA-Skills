#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化函数
"""

from typing import Dict, Any, List
try:
    from utils import calculate_discount, format_price
except ImportError:
    from .utils import calculate_discount, format_price


def format_goods_item(goods: Dict[str, Any]) -> str:
    """
    格式化单个商品信息

    Args:
        goods: 商品信息字典

    Returns:
        格式化后的商品信息字符串
    """
    goods_name = goods.get('goods_name', goods.get('title', '未知商品'))
    original_price = goods.get('originalPrice', goods.get('original_price', goods.get('price', 0)))
    final_price = goods.get('price', 0)
    goods_link = goods.get('link', '')
    month_sales = goods.get('monthSales', goods.get('sales', ''))
    coupon_price = goods.get('couponPrice', goods.get('couponAmount', 0))

    # 优惠券信息
    coupon_info = '暂无'
    if coupon_price and float(coupon_price) > 0:
        coupon_info = f'满减¥{float(coupon_price):.0f}'
    else:
        alt_coupon = goods.get('coupon', goods.get('couponInfo', ''))
        if alt_coupon:
            coupon_info = str(alt_coupon)

    save_amount = original_price - final_price if original_price > final_price else 0

    output = f"商品名称：{goods_name}\n"
    output += f"原价：{format_price(original_price)}\n"
    output += f"券后价：{format_price(final_price)}\n"
    output += f"优惠券：{coupon_info}\n"
    if month_sales:
        sales_str = str(month_sales)
        if not sales_str.endswith('+') and not sales_str.endswith('件') and not sales_str.endswith('万'):
            try:
                n = int(sales_str)
                if n >= 10000:
                    sales_str = f'{n/10000:.0f}万+'
                else:
                    sales_str = f'{n}件'
            except (ValueError, TypeError):
                pass
        output += f"月销量：{sales_str}\n"

    # 国补信息
    gov_subsidy = goods.get('gov_subsidy')
    if gov_subsidy:
        tag = gov_subsidy.get('tag_name', '国家补贴')
        info = gov_subsidy.get('state_subsidy_info', {})
        max_discount = info.get('max_discount', '')
        max_rebate = info.get('max_rebate', '')
        provinces = info.get('province_list', {}).get('string', [])
        parts = [f"🏷️ {tag}"]
        if max_rebate:
            parts.append(f"最高{max_rebate}%")
        if max_discount:
            parts.append(f"省¥{max_discount}")
        if provinces:
            parts.append(f"{len(provinces)}省可用")
        output += '：'.join(parts) + '\n'

    if goods_link:
        output += f"优惠链接：[点击跳转]({goods_link})\n"
    else:
        output += f"优惠链接：暂无\n"

    return output


def format_search_results(results: List[Dict[str, Any]], keyword: str) -> str:
    """
    格式化搜索结果

    Args:
        results: 搜索结果列表
        keyword: 搜索关键词

    Returns:
        格式化后的搜索结果字符串
    """
    if not results:
        return f"❌ 未找到与「{keyword}」相关的商品\n\n💡 建议：\n• 尝试更换关键词\n• 使用更通用的搜索词"

    output = f"🔍 找到 {len(results)} 个相关商品：\n\n"

    for idx, goods in enumerate(results, 1):
        output += format_goods_item(goods)
        output += "\n---\n\n"

    total_save = sum(g.get('save_amount', 0) for g in results if g.get('save_amount', 0) > 0)
    if total_save > 0:
        output += f"💡 已为您找到最优惠价格，预计节省 {format_price(total_save)}"

    return output


def format_convert_result(result: Dict[str, Any]) -> str:
    """
    格式化链接转换结果

    Args:
        result: 转换结果

    Returns:
        格式化后的转换结果字符串
    """
    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 转换失败：{error}"

    goods_name = result.get('goods_name') or result.get('title') or result.get('goodsName') or '未知商品'
    original_price = result.get('original_price', result.get('price', 0))
    final_price = result.get('final_price', result.get('price', 0))
    save_amount = result.get('save_amount', 0)
    promotion_link = result.get('short_url') or result.get('url') or result.get('promotion_link', '')
    coupon_info = result.get('coupon_info', '暂无')

    if save_amount == 0 and original_price > final_price:
        save_amount = original_price - final_price

    output = "✅ 优惠链接已生成\n\n"
    output += f"商品名称：{goods_name}\n"
    output += f"原价：{format_price(original_price)}\n"
    output += f"券后价：{format_price(final_price)}\n"
    output += f"优惠券：{coupon_info}\n"
    if promotion_link:
        output += f"优惠链接：[点击跳转]({promotion_link})\n"
    else:
        output += f"优惠链接：暂无\n"

    if save_amount > 0:
        output += f"\n💡 使用此链接购买，预计节省 {format_price(save_amount)}"

    return output


def format_parse_result(result: Dict[str, Any], platform: str) -> str:
    """
    格式化解析结果

    Args:
        result: 解析结果
        platform: 平台名称

    Returns:
        格式化后的解析结果字符串
    """
    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 口令解析失败\n\n可能的原因：\n• 口令已过期（通常7-15天有效期）\n• 口令格式不正确\n• 商品已下架\n\n💡 建议：\n• 重新获取最新的分享口令\n• 或直接发送商品链接"

    data = result.get('data', result)
    goods_name = data.get('goods_name', data.get('item_name', '未知商品'))
    original_price = data.get('original_price', data.get('price', 0))
    final_price = data.get('final_price', data.get('price', 0))
    save_amount = data.get('save_amount', 0)
    promotion_link = data.get('short_url') or data.get('url') or data.get('promotion_link', data.get('item_link', ''))
    coupon_info = data.get('coupon_info', '暂无')

    if save_amount == 0 and original_price > final_price:
        save_amount = original_price - final_price

    output = "✅ 商品信息已解析\n\n"
    output += f"商品名称：{goods_name}\n"
    output += f"原价：{format_price(original_price)}\n"
    output += f"券后价：{format_price(final_price)}\n"
    output += f"优惠券：{coupon_info}\n"
    if promotion_link:
        output += f"优惠链接：[点击跳转]({promotion_link})\n"
    else:
        output += f"优惠链接：暂无\n"

    if save_amount > 0:
        output += f"\n💡 预计节省：{format_price(save_amount)}"

    return output


def format_compare_result(result: Dict[str, Any]) -> str:
    """
    格式化价格对比结果

    Args:
        result: 对比结果

    Returns:
        格式化后的对比结果字符串
    """
    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 价格对比失败：{error}"

    comparison = result.get('comparison', [])
    cheapest = result.get('cheapest', {})

    if not comparison:
        return "❌ 未找到可对比的商品信息"

    output = "📊 价格对比结果\n\n"

    max_save = 0
    for item in comparison:
        platform = item.get('platform', '未知平台')
        goods_name = item.get('goods_name', '未知商品')
        original_price = item.get('original_price', item.get('price', 0))
        final_price = item.get('final_price', item.get('price', 0))
        save_amount = item.get('save_amount', 0)
        promotion_link = item.get('short_url') or item.get('url') or item.get('promotion_link', item.get('goods_link', ''))
        coupon_info = item.get('coupon_info', '暂无')

        if save_amount == 0 and original_price > final_price:
            save_amount = original_price - final_price

        if save_amount > max_save:
            max_save = save_amount

        output += f"【{platform}】\n"
        output += f"商品名称：{goods_name}\n"
        output += f"原价：{format_price(original_price)}\n"
        output += f"券后价：{format_price(final_price)}\n"
        output += f"优惠券：{coupon_info}\n"
        if promotion_link:
            output += f"优惠链接：[点击跳转]({promotion_link})\n"
        else:
            output += f"优惠链接：暂无\n"
        output += "\n---\n\n"

    if cheapest:
        cheapest_platform = cheapest.get('platform', '未知平台')
        cheapest_price = cheapest.get('price', 0)
        output += f"💡 最优惠推荐：{cheapest_platform} 券后价 {format_price(cheapest_price)}"
        if max_save > 0:
            output += f"，节省 {format_price(max_save)}"

    return output


def format_error_message(error_type: str, **kwargs) -> str:
    """
    格式化错误消息

    Args:
        error_type: 错误类型
        **kwargs: 其他参数

    Returns:
        格式化后的错误消息字符串
    """
    error_templates = {
        'parse_failed': """❌ 口令解析失败

可能的原因：
• 口令已过期（通常7-15天有效期）
• 口令格式不正确
• 商品已下架

💡 建议：
• 重新获取最新的分享口令
• 或直接发送商品链接""",

        'invalid_link': """❌ 无法识别的链接格式

支持的链接格式：
• 京东: item.jd.com/xxx.html
• 淘宝: item.taobao.com/item.htm?id=xxx
• 拼多多: mobile.yangkeduo.com/goods.html?goods_id=xxx

💡 请检查链接是否完整""",

        'no_results': """❌ 未找到相关商品

💡 建议：
• 尝试更换关键词
• 使用更通用的搜索词
• 检查是否有拼写错误""",

        'api_error': """⚠️ 系统繁忙，请稍后重试

如果问题持续，请联系管理员""",

        'platform_not_supported': """❌ 不支持的平台

支持的平台：
• 京东 (jd)
• 淘宝 (taobao)
• 拼多多 (pinduoduo)"""
    }

    return error_templates.get(error_type, f"❌ 发生错误：{error_type}")
