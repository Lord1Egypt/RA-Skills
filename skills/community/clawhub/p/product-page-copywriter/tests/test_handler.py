#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ProductPageCopywriter, handle


def test_platform_detection_jd():
    writer = ProductPageCopywriter('Create JD product page copy for a new kitchen appliance.')
    assert writer.platform == 'JD'


def test_tone_detection_compliance():
    writer = ProductPageCopywriter('Need compliant copy with legal review because this category is sensitive.')
    assert writer.tone == 'Compliant / cautious'


def test_render_contains_sections():
    output = handle('Write conversion-led PDP copy for a travel bottle with portable and safe design benefits.')
    assert output.startswith('# Product Page Copy Pack')
    assert '## Title Candidates' in output
    assert '## Compliance Watchouts' in output


def test_dict_input_supported():
    output = handle({
        'product_name': 'Aurora Travel Mug',
        'platform': 'Tmall',
        'benefits': ['portable', 'easy to clean', 'premium feel'],
    })
    assert '# Product Page Copy Pack' in output
    assert 'Aurora Travel Mug' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
