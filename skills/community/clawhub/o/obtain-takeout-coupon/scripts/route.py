
import asyncio
import aiohttp
import argparse

# 网关服务配置
GATEWAY_BASE_URL = "https://agskills.moontai.top"


SESSION: aiohttp.ClientSession | None = None

async def get_meituan_coupon() -> dict:
    """调用美团优惠券接口"""
    try:
        async with SESSION.get(f"{GATEWAY_BASE_URL}/coupon/takeout") as resp:
            data = await resp.json()
            return data
    except Exception as e:
        return {"error": str(e), "code": 500}

async def get_eleme_coupon() -> dict:
    """调用闪购优惠券接口"""
    try:
        async with SESSION.get(f"{GATEWAY_BASE_URL}/coupon/takeout") as resp:
            data = await resp.json()
            return data
    except Exception as e:
        return {"error": str(e), "code": 500}


async def obtain_coupon(keyword, source, page):
    """获取外卖优惠券，统一使用 /coupon/takeout 接口"""
    # 所有平台都使用统一的接口
    return await get_meituan_coupon()

    



async def main():
    global SESSION
    async with aiohttp.ClientSession as SESSION:
        parser = argparse.ArgumentParser()
        parsers = parser.add_subparsers()

        search_parser = parsers.add_parser("search")
        search_parser.add_argument("--source", default="1")
        search_parser.set_defaults(func=obtain_coupon)


        args = parser.parse_args()
        if hasattr(args, "func"):
            print(await args.func(**vars(args)))
        else:
            parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())