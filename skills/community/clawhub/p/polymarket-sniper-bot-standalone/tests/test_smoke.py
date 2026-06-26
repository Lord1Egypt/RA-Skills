def test_import_sniper_module():
    """Smoke test: ensure the polymarket module imports without error."""
    import scripts.polymarket as sniper
    assert hasattr(sniper, 'get_config')
    assert hasattr(sniper, 'IS_LIVE')
    assert hasattr(sniper, 'place_order')
