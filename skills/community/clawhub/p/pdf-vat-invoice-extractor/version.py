"""
v2.4.7 稳定版（2026-10-29）
这是 pdf-invoice-stat skill 的单一版本真相源（SSOT）。
所有文档和代码应从此导入 __version__。

v2.4.7 = v2.4.6 + 铁路电子客票特殊规则
  - 退票费属价外费用，不征增值税：金额=价税合计、税额=0、税率列留空
  - 铁路电子客票无销售方栏，填「中国铁路（铁路客运服务）」作口径标注
支持 PDF / XML / OFD / ZIP / RAR 五种格式，PDF 主路径核心逻辑未变。
"""
__version__ = "2.4.7"
__version_info__ = (2, 4, 7)
__release_date__ = "2026-10-29"
__status__ = "stable"
__description__ = "PDF/XML/OFD/ZIP/RAR 增值税发票提取 v2.4.7（稳定版）"
__formats__ = ["PDF", "XML", "OFD", "ZIP", "RAR"]
