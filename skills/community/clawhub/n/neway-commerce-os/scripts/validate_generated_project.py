#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_FILES = [
    "package.json",
    "index.html",
    "src/main.tsx",
    "src/App.tsx",
    "src/components/Navbar.tsx",
    "src/components/Footer.tsx",
    "src/components/ProductCard.tsx",
    "src/components/CartDrawer.tsx",
    "src/components/AIChatWidget.tsx",
    "src/pages/HomePage.tsx",
    "src/pages/ShopPage.tsx",
    "src/pages/ProductPage.tsx",
    "src/pages/CartPage.tsx",
    "src/pages/CheckoutPage.tsx",
    "src/pages/WishlistPage.tsx",
    "src/pages/AdminPage.tsx",
    "src/types/index.ts",
    "src/data/products.ts",
]

# Style/Store files: accept common naming variants
STYLE_VARIANTS = ["src/styles.css", "src/index.css"]
STORE_VARIANTS = ["src/store/cartStore.ts", "src/store/index.ts"]

# Deployment/backend files: warn if missing, but don't block
DEPLOYMENT_FILES = [
    "functions/api/products.ts",
    "functions/api/checkout.ts",
    "functions/api/assistant.ts",
    "functions/node/stripe-webhook.ts",
    ".env.example",
    "edgeone.json",
]

FORBIDDEN_FILES = [
    "src/pages/AccountPage.tsx",
    "src/components/AiConcierge.tsx",
    "src/data/products.json",
    "src/lib/api.ts",
]

PLACEHOLDERS = [
    "__SITE_NAME__",
    "__BRAND_NAME__",
    "__SITE_SLUG__",
    "__PROMPT__",
]

# Product interface fields that MUST be present in types/index.ts
REQUIRED_PRODUCT_FIELDS = [
    "id",
    "name",
    "nameEn",
    "origin",
    "price",
    "originalPrice",
    "unit",
    "images",
    "category",
    "tags",
    "weight",
    "sweetness",
    "description",
    "highlight",
    "isNew",
    "isSale",
    "isOrganic",
    "rating",
    "reviewCount",
    "stock",
]

# Pages that must have certain minimum content indicators
PAGE_MINIMUM_INDICATORS = {
    "src/pages/HomePage.tsx": [
        "AnimatePresence",   # carousel
        "categories",         # category banners
        "isNew",              # seasonal/new section
        "rating",             # bestsellers section
    ],
    "src/pages/ShopPage.tsx": [
        "category",           # category tabs
        "sort",               # sort dropdown
        "filter",             # filter panel
        "grid", "list",       # grid/list toggle
    ],
    "src/pages/ProductPage.tsx": [
        "images[", "images.",  # image gallery (multi-image)
        "sweetness",          # sweetness/quality meter
        "favorite", "wishlist", # heart/favorite button
    ],
}

# Wishlist check will search store files dynamically

def validate_project(project_dir: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Required files check
    for rel in REQUIRED_FILES:
        target = project_dir / rel
        if not target.exists():
            errors.append(f"Missing required file: {rel}")

    # 1b. Variant file checks (accept any one variant)
    if not any((project_dir / v).exists() for v in STYLE_VARIANTS):
        errors.append(f"Missing style file (expected one of: {STYLE_VARIANTS})")
    if not any((project_dir / v).exists() for v in STORE_VARIANTS):
        errors.append(f"Missing cart store file (expected one of: {STORE_VARIANTS})")

    # 1c. Deployment files — warn only
    for rel in DEPLOYMENT_FILES:
        target = project_dir / rel
        if not target.exists():
            warnings.append(f"Missing deployment file (optional for demo): {rel}")

    # 2. Forbidden files check (template leftovers)
    for rel in FORBIDDEN_FILES:
        target = project_dir / rel
        if target.exists():
            errors.append(f"Uncleaned template file must be deleted: {rel}")

    # 3. Placeholder check
    for file_path in project_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.name.endswith(".tsbuildinfo"):
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in PLACEHOLDERS:
            if token in content:
                errors.append(f"Unreplaced placeholder {token} in {file_path.relative_to(project_dir)}")

    # 4. Product type fields check
    types_file = project_dir / "src" / "types" / "index.ts"
    if types_file.exists():
        types_content = types_file.read_text(encoding="utf-8")
        missing_fields = [f for f in REQUIRED_PRODUCT_FIELDS if f not in types_content]
        if missing_fields:
            warnings.append(f"Product type missing fields: {', '.join(missing_fields)}")

    # 5. Page minimum complexity check
    for page_rel, indicators in PAGE_MINIMUM_INDICATORS.items():
        page_path = project_dir / page_rel
        if not page_path.exists():
            continue
        page_content = page_path.read_text(encoding="utf-8")
        missing_indicators = [i for i in indicators if i not in page_content]
        if missing_indicators:
            warnings.append(f"{page_rel} may be below quality floor: missing indicators {missing_indicators}")

    # 6. Cart store persist check
    cart_path = None
    for v in STORE_VARIANTS:
        p = project_dir / v
        if p.exists():
            cart_path = p
            break
    if cart_path and cart_path.exists():
        cart_content = cart_path.read_text(encoding="utf-8")
        for keyword in ["persist", "addItem", "removeItem", "updateQty", "clearCart", "total", "count"]:
            if keyword not in cart_content:
                errors.append(f"Cart store ({cart_path.name}) missing: {keyword}")

    # 7. Wishlist persistence check (search in both store files and wishlist page)
    wishlist_persist_found = False
    for store_rel in STORE_VARIANTS:
        store_path = project_dir / store_rel
        if store_path.exists():
            content = store_path.read_text(encoding="utf-8")
            if "wishlist" in content.lower() and "persist" in content:
                wishlist_persist_found = True
                break
    if not wishlist_persist_found:
        # Also check if there's a separate wishlist store
        for f in (project_dir / "src" / "store").rglob("*.ts"):
            content = f.read_text(encoding="utf-8")
            if "wishlist" in content.lower() and "persist" in content:
                wishlist_persist_found = True
                break
    if not wishlist_persist_found:
        warnings.append("No wishlistStore with persist found. WishlistState should use Zustand+persist, not local useState.")

    # 8. Color palette check
    tailwind_config = project_dir / "tailwind.config.js"
    if tailwind_config.exists():
        tw_content = tailwind_config.read_text(encoding="utf-8")
        has_palette_count = sum(1 for p in ["brand:", "leaf:", "fresh:", "accent:"] if p in tw_content)
        if has_palette_count < 2:
            warnings.append("tailwind.config.js should define at least 2 color palettes (e.g. brand + leaf/fresh)")
        if "50:" not in tw_content or "900:" not in tw_content:
            warnings.append("Color palettes should have full 50-950 scale")

    # 9. CSS component classes check
    styles_path = None
    for v in STYLE_VARIANTS:
        p = project_dir / v
        if p.exists():
            styles_path = p
            break
    if styles_path:
        css_content = styles_path.read_text(encoding="utf-8")
        required_classes = ["btn-primary", "btn-outline", "btn-ghost", "tag", "input-field"]
        missing_css = [c for c in required_classes if f".{c}" not in css_content]
        if missing_css:
            warnings.append(f"styles.css missing component classes: {', '.join(missing_css)}")

    # Print results
    all_msgs = errors + warnings
    if errors:
        print("[FAIL] Quality gate errors:")
        for e in errors:
            print(f"  [ERR] {e}")
    if warnings:
        print("[WARN] Quality gate warnings:")
        for w in warnings:
            print(f"  [WARN] {w}")

    has_errors = len(errors) > 0
    if has_errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    elif warnings:
        print(f"\n[PASS] 0 errors, {len(warnings)} warning(s) — review warnings above")
    else:
        print("[PASS] All quality gates passed!")

    return (not has_errors, all_msgs)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python validate_generated_project.py <project_dir>")
        raise SystemExit(1)

    project_dir = Path(sys.argv[1]).resolve()
    if not project_dir.exists():
        print(f"Project not found: {project_dir}")
        raise SystemExit(1)

    ok, _ = validate_project(project_dir)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
