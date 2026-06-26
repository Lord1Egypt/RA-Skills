# pip install zai-sdk # 安装最新版本
# pip install zai-sdk==0.0.3.3 # 或指定版本

#import zai print(zai.__version__) # 验证安装
from zai import ZhipuAiClient

import base64
import os
import re
URL_PATTERN = re.compile(
    r'^(?:http|ftp)s?://'  # 协议头（http/https/ftp/ftps）
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名（如baidu.com、www.abc.co.uk）
    r'localhost|'  # 本地主机
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP地址（如192.168.1.1）
    r'(?::\d+)?'  # 可选端口（如:8080）
    r'(?:/?|[/?]\S+)$',  # 可选路径/参数/锚点（如/index.html?a=1#top）
    re.IGNORECASE  # 忽略大小写（如HTTP/https均可）
)

def is_url_by_regex(text: str) -> bool:
    """
    用正则判断字符串是否为合法URL
    :param text: 待判断的字符串
    :return: True=是URL，False=不是
    """
    if not isinstance(text, str) or len(text.strip()) == 0:
        return False
    # 匹配整个字符串（避免只匹配部分内容，比如"abchttps://baidu.comdef"）
    return bool(URL_PATTERN.fullmatch(text.strip()))

api_key = os.environ.get("ZHIPU_API_KEY")
client = ZhipuAiClient(api_key=api_key)  # 填写您自己的APIKey

def glm_v(imagelists, prompt = 'descript these pictures', model='glm-4.6v', type = 'enabled'):
    content = []
    for img in imagelists:
        if is_url_by_regex(img):
            content.append({"type": "image_url", "image_url":{"url": img}})
        else:
            img_base = base64.b64encode(img.read()).decode("utf-8")
            content.append({"type": "image_url", "image_url":{"url": img_base}})
    content.append({"type": "text", "content": prompt})

    response = client.chat.completions.create(
        model ="glm-4.6v",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        thinking={
            "type": "enabled"
        }
    )
    print(response.choices[0].message)
