"""Social account detector — WeChat, QQ, Twitter/X, and generic account patterns."""

import re
from .base import BaseDetector, Match


class SocialAccountDetector(BaseDetector):
    label = "SOCIAL_ACCOUNT"

    # WeChat ID after keyword: letter-start, 6-20 chars
    WECHAT = re.compile(
        r'(?:\u5fae\u4fe1|wechat|WeChat|wx)[\u53f7ID\uff1a:\s]*([a-zA-Z][\w\-]{5,19})',
        re.IGNORECASE
    )

    # QQ number after keyword: 5-12 digits
    QQ = re.compile(
        r'(?:QQ|qq)[\u53f7\uff1a:\s]*(\d{5,12})'
    )

    # Twitter / X handle
    TWITTER = re.compile(
        r'(?:twitter|\u63a8\u7279|X)[\uff1a:\s]*@?([a-zA-Z_][\w]{1,15})',
        re.IGNORECASE
    )

    # Generic: after "账号/帐号/account" keyword
    GENERIC = re.compile(
        r'(?:\u8d26\u53f7|\u5e10\u53f7|account)[\uff1a:\s]*([\w@.\-]{4,30})',
        re.IGNORECASE
    )

    def detect(self, text):
        matches = []
        seen = set()

        for pattern in [self.WECHAT, self.QQ, self.TWITTER, self.GENERIC]:
            for m in pattern.finditer(text):
                account = m.group(1)
                if account in seen:
                    continue
                seen.add(account)
                if len(account) > 4:
                    masked = account[:2] + '****' + account[-2:]
                else:
                    masked = account[:1] + '***'
                matches.append(Match(
                    label=self.label,
                    confidence=0.80,
                    masked_preview=masked,
                    start=m.start(1),
                    end=m.end(1),
                ))
        return matches
