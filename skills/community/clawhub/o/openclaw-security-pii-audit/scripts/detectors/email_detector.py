"""Email address detector."""

import re
from .base import BaseDetector, Match


class EmailDetector(BaseDetector):
    label = "EMAIL"

    PATTERN = re.compile(
        r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
        re.ASCII
    )

    def detect(self, text):
        matches = []
        for m in self.PATTERN.finditer(text):
            raw = m.group()
            local, domain = raw.rsplit('@', 1)
            masked = self._mask(local, 2, 0) + '@' + domain
            matches.append(Match(
                label=self.label,
                confidence=0.95,
                masked_preview=masked,
                start=m.start(),
                end=m.end(),
            ))
        return matches
