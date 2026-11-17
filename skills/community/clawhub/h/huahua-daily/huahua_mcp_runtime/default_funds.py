"""App default fund catalogs mirrored into the standalone MCP package.

The MCP runtime is distributed independently from the React application, so it
cannot import ``src/shared/defaultFundLists.ts`` at runtime.  A repository
contract test keeps this generated mirror byte-for-byte aligned with the App's
canonical catalog.
"""

DEFAULT_NIGHT_FUNDS: tuple[tuple[str, str], ...] = (
    ("022184", "富国全球科技互联网股票(QDII)C"),
    ("024239", "华夏全球科技先锋混合(QDII)C"),
    ("018147", "建信新兴市场混合(QDII)C"),
    ("012922", "易方达全球成长精选混合(QDII)人民币C"),
    ("016665", "天弘全球高端制造混合(QDII)C"),
    ("017731", "嘉实全球产业升级股票发起式(QDII)C"),
    ("017437", "华宝纳斯达克精选股票发起式(QDII)C"),
    ("021277", "广发全球精选股票(QDII)人民币C"),
    ("008254", "华宝致远混合(QDII)C"),
    ("016702", "银华海外数字经济量化选股混合发起式(QDII)C"),
    ("021842", "国富全球科技互联混合(QDII)人民币C"),
    ("006479", "广发纳斯达克100ETF联接人民币(QDII)C"),
)

DEFAULT_NIGHT_FUND_CODES: tuple[str, ...] = tuple(
    code for code, _name in DEFAULT_NIGHT_FUNDS
)
