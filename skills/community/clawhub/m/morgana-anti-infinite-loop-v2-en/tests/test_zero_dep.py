"""PROVE that anti-loop v2.0 works WITHOUT numpy (zero-dep CORE claim)."""
import sys
import importlib.util


def test_no_numpy_required():
    """Simulate numpy not being available by blocking the import."""
    # Block numpy import
    saved = sys.modules.get('numpy')
    sys.modules['numpy'] = None
    
    try:
        # Load core.py directly (bypassing the anti_loop package)
        # to prove the underlying module has zero hard dependency on numpy.
        spec = importlib.util.spec_from_file_location(
            "_core_under_test",
            "/mnt/Morgana/skills/morgana-anti-infinite-loop-v2/anti_loop/core.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # If we get here, it loaded without numpy
        guard = mod.AntiLoop(mode="heal")
        result = guard.observe("test action", "find X")
        assert result["iteration"] == 1
        assert result["novelty"] >= 0
        assert result["entropy"] >= 0
    finally:
        if saved is not None:
            sys.modules['numpy'] = saved
        else:
            sys.modules.pop('numpy', None)


if __name__ == "__main__":
    test_no_numpy_required()
    print("✅ ZERO-DEP PROOF: anti_loop.core works without numpy")
