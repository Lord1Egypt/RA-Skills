#!/usr/bin/env python3
"""
腾讯云 TLSSigAPIv2 — 官方 UserSig 生成算法
源自: https://github.com/tencentyun/tls-sig-api-v2-python/blob/master/TLSSigAPIv2.py

用于签发 TRTC 和 IM 服务中必须使用的 UserSig 鉴权票据。
⚠️ 安全提醒：请勿将此代码及 SecretKey 部署在客户端（App、Web 前端），
   SecretKey 一旦泄露，攻击者可以盗用您的流量。
   正式上线时，UserSig 应由后端服务生成后下发给客户端。
"""
import hmac
import hashlib
import base64
import zlib
import json
import time


def base64_encode_url(data):
    """base64 url-safe 编码（腾讯云定制变体）"""
    base64_data = base64.b64encode(data)
    base64_data_str = bytes.decode(base64_data)
    base64_data_str = base64_data_str.replace('+', '*')
    base64_data_str = base64_data_str.replace('/', '-')
    base64_data_str = base64_data_str.replace('=', '_')
    return base64_data_str


def base64_decode_url(base64_data):
    """base64 url-safe 解码（腾讯云定制变体）"""
    base64_data_str = bytes.decode(base64_data)
    base64_data_str = base64_data_str.replace('*', '+')
    base64_data_str = base64_data_str.replace('-', '/')
    base64_data_str = base64_data_str.replace('_', '=')
    raw_data = base64.b64decode(base64_data_str)
    return raw_data


class TLSSigAPIv2:
    """腾讯云 TLSSigAPIv2 UserSig 生成器

    使用方法:
        api = TLSSigAPIv2(sdkappid, secret_key)
        sig = api.genUserSig("user123", expire=604800)  # 7天有效期
    """
    __sdkappid = 0
    __version = '2.0'
    __key = ""

    def __init__(self, sdkappid, key):
        self.__sdkappid = sdkappid
        self.__key = key

    def _gen_userbuf(self, account, dwAuthID, dwExpTime,
                     dwPrivilegeMap, dwAccountType, roomStr):
        """生成 userbuf（用于 PrivateMapKey 权限票据）"""
        userBuf = b''
        if len(roomStr) > 0:
            userBuf += bytearray([1])
        else:
            userBuf += bytearray([0])

        userBuf += bytearray([
            ((len(account) & 0xFF00) >> 8),
            (len(account) & 0x00FF),
        ])
        userBuf += bytearray(map(ord, account))

        # dwSdkAppid
        userBuf += bytearray([
            ((self.__sdkappid & 0xFF000000) >> 24),
            ((self.__sdkappid & 0x00FF0000) >> 16),
            ((self.__sdkappid & 0x0000FF00) >> 8),
            (self.__sdkappid & 0x000000FF),
        ])
        # dwAuthId
        userBuf += bytearray([
            ((dwAuthID & 0xFF000000) >> 24),
            ((dwAuthID & 0x00FF0000) >> 16),
            ((dwAuthID & 0x0000FF00) >> 8),
            (dwAuthID & 0x000000FF),
        ])
        # dwExpTime
        expire = dwExpTime + int(time.time())
        userBuf += bytearray([
            ((expire & 0xFF000000) >> 24),
            ((expire & 0x00FF0000) >> 16),
            ((expire & 0x0000FF00) >> 8),
            (expire & 0x000000FF),
        ])
        # dwPrivilegeMap
        userBuf += bytearray([
            ((dwPrivilegeMap & 0xFF000000) >> 24),
            ((dwPrivilegeMap & 0x00FF0000) >> 16),
            ((dwPrivilegeMap & 0x0000FF00) >> 8),
            (dwPrivilegeMap & 0x000000FF),
        ])
        # dwAccountType
        userBuf += bytearray([
            ((dwAccountType & 0xFF000000) >> 24),
            ((dwAccountType & 0x00FF0000) >> 16),
            ((dwAccountType & 0x0000FF00) >> 8),
            (dwAccountType & 0x000000FF),
        ])

        if len(roomStr) > 0:
            userBuf += bytearray([
                ((len(roomStr) & 0xFF00) >> 8),
                (len(roomStr) & 0x00FF),
            ])
            userBuf += bytearray(map(ord, roomStr))

        return userBuf

    def __hmacsha256(self, identifier, curr_time, expire,
                     base64_userbuf=None):
        """通过固定串进行 HMAC-SHA256 签名"""
        raw_content_to_be_signed = (
            "TLS.identifier:" + str(identifier) + "\n"
            + "TLS.sdkappid:" + str(self.__sdkappid) + "\n"
            + "TLS.time:" + str(curr_time) + "\n"
            + "TLS.expire:" + str(expire) + "\n"
        )
        if base64_userbuf is not None:
            raw_content_to_be_signed += (
                "TLS.userbuf:" + base64_userbuf + "\n"
            )

        return base64.b64encode(
            hmac.new(
                self.__key.encode('utf-8'),
                raw_content_to_be_signed.encode('utf-8'),
                hashlib.sha256
            ).digest()
        )

    def __gen_sig(self, identifier, expire=180 * 86400, userbuf=None):
        """内部签名生成"""
        curr_time = int(time.time())
        m = dict()
        m["TLS.ver"] = self.__version
        m["TLS.identifier"] = str(identifier)
        m["TLS.sdkappid"] = int(self.__sdkappid)
        m["TLS.expire"] = int(expire)
        m["TLS.time"] = int(curr_time)
        base64_userbuf = None
        if userbuf is not None:
            base64_userbuf = bytes.decode(base64.b64encode(userbuf))
            m["TLS.userbuf"] = base64_userbuf
        m["TLS.sig"] = bytes.decode(
            self.__hmacsha256(identifier, curr_time, expire, base64_userbuf)
        )
        raw_sig = json.dumps(m)
        sig_compressed = zlib.compress(raw_sig.encode('utf-8'))
        base64_sig = base64_encode_url(sig_compressed)
        return base64_sig

    def genUserSig(self, userid, expire=180 * 86400):
        """生成 UserSig 鉴权票据

        Args:
            userid: 用户 ID，长度不超过 32 字节，
                    只允许包含大小写英文字母、数字、下划线和连词符
            expire: 有效期（秒），默认 180 天。
                    建议开发调试阶段设为 604800（7天）
        Returns:
            UserSig 字符串
        """
        return self.__gen_sig(userid, expire, None)

    def genPrivateMapKey(self, userid, expire, roomid, privilegeMap):
        """生成 PrivateMapKey 权限票据（数字房间号）"""
        userbuf = self._gen_userbuf(
            userid, roomid, expire, privilegeMap, 0, ""
        )
        return self.__gen_sig(userid, expire, userbuf)

    def genPrivateMapKeyWithStringRoomID(self, userid, expire,
                                         roomstr, privilegeMap):
        """生成 PrivateMapKey 权限票据（字符串房间号）"""
        userbuf = self._gen_userbuf(
            userid, 0, expire, privilegeMap, 0, roomstr
        )
        return self.__gen_sig(userid, expire, userbuf)


# ── 便捷函数（供 setup.py 直接调用）─────────────────────────
def gen_usersig(sdkappid: int, secret: str, userid: str,
                expire: int = 604800) -> str:
    """生成 TRTC UserSig 的便捷包装

    Args:
        sdkappid: TRTC SDKAppID
        secret:   TRTC SecretKey
        userid:   用户 ID
        expire:   有效期（秒），默认 7 天
    Returns:
        UserSig 字符串
    """
    api = TLSSigAPIv2(sdkappid, secret)
    return api.genUserSig(userid, expire)


if __name__ == "__main__":
    # 使用示例（请替换为您的真实参数）
    import sys
    if len(sys.argv) >= 4:
        appid = int(sys.argv[1])
        key = sys.argv[2]
        uid = sys.argv[3]
        expire = int(sys.argv[4]) if len(sys.argv) > 4 else 604800
        sig = gen_usersig(appid, key, uid, expire)
        print(f"UserSig ({expire}s): {sig}")
    else:
        print("Usage: TLSSigAPIv2.py <sdkappid> <secret> <userid> [expire]")
        print("Example: TLSSigAPIv2.py 1400000000 your_secret_key user123")
