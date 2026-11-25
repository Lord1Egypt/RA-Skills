"""Run: python3 tests/test_tax.py  (from the skill folder)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from tax import compute, hra_exemption

def nt(**k): return compute(k)["new_regime"]["total_tax"]
def ot(**k): return compute(k)["old_regime"]["total_tax"]
cases = [
    ("12.75L salary is tax-free (new)",          nt(salary=1275000, age=30), 0),
    ("12L taxable exactly is tax-free (new)",     nt(other_income=1200000, age=30), 0),
    ("12.1L: marginal relief caps tax at 10k",    nt(other_income=1210000, age=30), 10400),
    ("13L: normal slab tax 75k + cess",           nt(other_income=1300000, age=30), 78000),
    ("60L: 10% surcharge",                        nt(other_income=6000000, age=30), 1578720),
    ("50.1L: surcharge marginal relief",          nt(other_income=5010000, age=30), 1133600),
    ("old 7L taxable: 52.5k + cess",              ot(other_income=700000, age=30), 54600),
    ("old 5L taxable: rebate makes it zero",      ot(other_income=500000, age=30), 0),
    ("old 60-79 gets 3L exemption",               ot(other_income=400000, age=65), 0),
    ("HRA in Pune (50% city)",                    round(hra_exemption({"basic_da":720000,"hra_received":360000,"rent_paid":300000,"city":"Pune"})), 228000),
    ("HRA in Jaipur (40%)",                       round(hra_exemption({"basic_da":720000,"hra_received":360000,"rent_paid":400000,"city":"Jaipur"})), 288000),
]
fail = 0
for name, got, want in cases:
    ok = got == want; fail += not ok
    print(("PASS " if ok else "FAIL ") + f"{name}: got {got}, expected {want}")
print("\nall passed" if not fail else f"\n{fail} failed"); sys.exit(fail)
