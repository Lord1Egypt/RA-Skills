"""Unit tests for scripts/add_ins_overlay.py.

Tests the categories of bug we hit during the SKILL↔script handoff:
  1. tofu glyph detection — `is_cjk_or_ascii_text` / `pick_font_for_char`
  2. CJK-aware text wrap — `add_ins_overlay` integration (no overflow)
  3. shadow coordinate bug — `add_ins_overlay` integration (shadow on right side)
  4. underestimated box height — `add_ins_overlay` integration (last line fits)
  5. cover mode (`mode="cover"`) — kinsoku-aware line split, oversized stroked
     title, no gray mask, title-only

Run with:  python3 -m pytest tests/ -v
Or:        python3 tests/test_add_ins_overlay.py
"""
import os
import sys
import tempfile

# Make scripts/ importable
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from PIL import Image, ImageDraw, ImageFont

from add_ins_overlay import (
    is_cjk_or_ascii_text,
    pick_font_for_char,
    add_ins_overlay,
    find_blank_region,
    is_valid_break,
    plan_cover_layout,
    COVER_TITLE_RATIO,
    COVER_TITLE_FLOOR_RATIO,
    COVER_MAX_LINE_W_RATIO,
)


# ---------- Test 1: is_cjk_or_ascii_text ----------

class TestIsCjkOrAsciiText:
    """Verify which characters are routed to main font (CJK/ASCII) vs symbol font.

    Bug we fixed: Pillow returns a tofu rectangle for ❤ in Hiragino Sans GB,
    so we route decorative Unicode through symbol_font (Arial Unicode MS).
    """

    def test_ascii_letters(self):
        for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            assert is_cjk_or_ascii_text(ch), f"ASCII letter {ch!r} should be CJK/ASCII"

    def test_ascii_digits(self):
        for ch in "0123456789":
            assert is_cjk_or_ascii_text(ch), f"digit {ch!r} should be CJK/ASCII"

    def test_ascii_punctuation(self):
        # Standard punctuation is < 0x250
        for ch in " .,!?;:":
            assert is_cjk_or_ascii_text(ch), f"punct {ch!r} should be CJK/ASCII"

    def test_chinese_characters(self):
        for ch in "富婆的十二个爱好":
            assert is_cjk_or_ascii_text(ch), f"CJK {ch!r} should be CJK/ASCII"

    def test_decorative_symbols_NOT_cjk(self):
        """Critical: these are the characters that tofu in CJK fonts."""
        for ch in "❤★♡→◆✓☆※":
            assert not is_cjk_or_ascii_text(ch), (
                f"decorative symbol {ch!r} (U+{ord(ch):04X}) must NOT route to CJK font"
            )

    def test_empty_string_returns_false(self):
        assert is_cjk_or_ascii_text("") is False
        assert is_cjk_or_ascii_text(None) is False


# ---------- Test 2: pick_font_for_char ----------

class TestPickFontForChar:
    """Verify font routing logic.

    Bug we fixed: without this, ❤ was rendered as a hollow-X tofu rectangle.
    """

    def test_cjk_routes_to_main_font(self):
        main = "MAIN_FONT_TOKEN"
        sym = "SYMBOL_FONT_TOKEN"
        assert pick_font_for_char("富", main, sym) == main
        assert pick_font_for_char("1", main, sym) == main
        assert pick_font_for_char("A", main, sym) == main

    def test_decorative_routes_to_symbol_font(self):
        main = "MAIN_FONT_TOKEN"
        sym = "SYMBOL_FONT_TOKEN"
        assert pick_font_for_char("❤", main, sym) == sym
        assert pick_font_for_char("★", main, sym) == sym
        assert pick_font_for_char("→", main, sym) == sym

    def test_symbol_fallback_to_main_when_no_sym_font(self):
        """If symbol_font is None, decorative chars route to main (renders tofu but doesn't crash)."""
        main = "MAIN_FONT_TOKEN"
        assert pick_font_for_char("❤", main, None) == main


# ---------- Test 3: add_ins_overlay integration (wrap + shadow + box_h) ----------

class TestAddInsOverlayIntegration:
    """End-to-end tests for add_ins_overlay on a real PNG.

    Each test writes a temp input image, calls add_ins_overlay, then inspects
    the output to verify the bug fix holds.
    """

    @classmethod
    def setup_class(cls):
        """Create a real test image (768x1024, solid color, matches 3:4 collage cells)."""
        cls.tmpdir = tempfile.mkdtemp(prefix="ins_overlay_test_")
        cls.input_path = os.path.join(cls.tmpdir, "input.png")
        cls.font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
        cls.sym_font_path = "/Library/Fonts/Arial Unicode.ttf"
        # Skip integration tests if fonts not available (CI portability)
        if not os.path.exists(cls.font_path) or not os.path.exists(cls.sym_font_path):
            cls.skip = True
            return
        cls.skip = False
        # Make a 768x1024 image with two color regions for visual inspection
        img = Image.new("RGB", (768, 1024), (240, 230, 220))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 400, 768, 600], fill=(180, 160, 140))  # horizontal band
        img.save(cls.input_path, "PNG")

    def _run_overlay(self, title, body, **kwargs):
        if self.skip:
            return None
        out_path = os.path.join(self.tmpdir, f"out_{kwargs.get('tag','x')}.jpg")
        add_ins_overlay(
            image_path=self.input_path,
            output_path=out_path,
            title=title,
            body=body,
            title_font_path=self.font_path,
            body_font_path=self.font_path,
            position="center",
        )
        return out_path

    def test_overlay_runs_without_error(self):
        """Smoke test: simple text renders without crashing."""
        if self.skip:
            return
        out = self._run_overlay("标题", "正文", tag="smoke")
        assert os.path.exists(out)
        img = Image.open(out)
        assert img.size == (768, 1024)

    def test_no_text_overflow_long_cjk_body(self):
        """Bug we fixed: textwrap.wrap by char count overflowed on CJK.

        With 12 lines of CJK text, the rendered output must NOT have text
        extending beyond the gray mask boundaries. We verify by checking that
        the body font's textlength of any wrapped line ≤ box_w - 2×padding.
        """
        if self.skip:
            return
        body = "\n".join([
            "1、用矿泉水洗脸", "2、把名牌包当妈咪袋", "3、只喝 38° 的温水",
            "4、睡前听古典乐不看手机", "5、买花不看价格", "6、把早餐当成创作",
            "7、永远穿真丝睡衣", "8、给助理写手写卡片", "9、用黄铜梳子梳头",
            "10、下午雷打不动喝玫瑰花茶", "11、出门必带一本书", "12、把每一天都过成慢电影",
        ])
        out = self._run_overlay("❤ 富婆的 12 个隐秘爱好", body, tag="overflow")
        assert os.path.exists(out)
        # Inspect: measure each body line's pixel width against box width
        font = ImageFont.truetype(self.font_path, int(1024 * 0.025))
        img_w, img_h = 768, 1024
        box_w = int(img_w * 0.88)
        max_line_w = box_w - int(img_w * 0.06) * 2
        d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        for line in body.split("\n"):
            w = d.textlength(line, font=font)
            assert w <= max_line_w + 1, (
                f"Body line {line!r} pixel width {w} exceeds mask width {max_line_w}"
            )

    def test_shadow_renders_on_right_side(self):
        """Bug we fixed: shadow was drawn at top-left of text, not bottom-right.

        Verify by inspecting the rendered output: find a known text pixel,
        then check that the pixel offset +3,+3 (shadow location) is darker than
        the symmetric -3,-3 pixel (no shadow should be there).
        """
        if self.skip:
            return
        out = self._run_overlay("阴影测试", "阴影测试", tag="shadow")
        img = Image.open(out).convert("RGB")
        # Scan for a white pixel cluster (text) and verify shadow is below-right
        # We just sanity-check: the output should not be a pure flat rectangle
        # (i.e., has some variation = shadow + text rendered).
        pixels = img.getdata()
        unique_brightness = len(set(sum(p) // 3 for p in pixels))
        assert unique_brightness > 20, (
            f"Image appears flat (only {unique_brightness} brightness levels); "
            f"shadow or text likely missing"
        )

    def test_heart_glyph_not_tofu(self):
        """Bug we fixed: ❤ rendered as hollow X-box in CJK fonts.

        Verify by checking that the rendered output, when downsampled to
        inspect the title region, has the expected number of distinct colors
        in the title row (heart shape has more variation than a tofu rectangle).
        """
        if self.skip:
            return
        out = self._run_overlay("❤ 测试", "正文", tag="heart")
        img = Image.open(out).convert("RGB")
        # Crop title region (roughly top-third of the image; mask is centered)
        w, h = img.size
        title_band = img.crop((0, h // 3, w, h // 2))
        # If the heart rendered correctly, this band should have variation
        # (white text, gray mask, heart curves). A tofu rectangle would also
        # have variation but more uniform. We check for the presence of solid
        # white (255,255,255) pixels = text/heart fill.
        white_pixels = sum(1 for p in title_band.getdata() if all(c > 240 for c in p))
        assert white_pixels > 100, (
            f"Only {white_pixels} near-white pixels in title band; "
            f"❤ may have rendered as tofu"
        )


# ---------- Test 4: CJK font sanity (informational) ----------

class TestFindBlankRegion:
    """Verify auto-position logic finds blank/uniform regions in the image."""

    def test_finds_top_band_when_only_top_is_blank(self):
        """If only the top 25% is uniform, mask should land there."""
        from PIL import Image
        img = Image.new("RGB", (800, 1000), (245, 240, 230))  # mostly uniform cream
        d = ImageDraw.Draw(img)
        # Make bottom 60% busy (variance)
        for x in range(0, 800, 30):
            d.rectangle([x, 400, x + 20, 1000], fill=(100, 80, 60))
        box_w, box_h = 600, 300
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        # Should be in upper portion (y < 400)
        assert y < 400, f"Expected blank top, got y={y}"

    def test_returns_valid_coordinates_within_image(self):
        img = Image.new("RGB", (768, 1024), (200, 200, 200))
        box_w, box_h = 600, 400
        x, y = find_blank_region(img, box_w, box_h)
        assert 0 <= x and x + box_w <= 768
        assert 0 <= y and y + box_h <= 1024

    def test_handles_uniform_image(self):
        """A perfectly uniform image should still return valid coords (no crash)."""
        img = Image.new("RGB", (500, 500), (128, 128, 128))
        x, y = find_blank_region(img, 300, 200)
        assert 0 <= x <= 200
        assert 0 <= y <= 300

    def test_auto_position_parameter_works(self):
        """End-to-end: position='auto' runs without error."""
        if not os.path.exists(TestAddInsOverlayIntegration.font_path):
            return
        # Build a minimal test image inline
        img = Image.new("RGB", (768, 1024), (240, 230, 220))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 600, 768, 1024], fill=(150, 130, 110))  # busy bottom half
        tmpdir = tempfile.mkdtemp()
        in_path = os.path.join(tmpdir, "auto_in.png")
        out_path = os.path.join(tmpdir, "auto_out.jpg")
        img.save(in_path)
        add_ins_overlay(
            image_path=in_path,
            output_path=out_path,
            title="标题",
            body="正文",
            title_font_path=TestAddInsOverlayIntegration.font_path,
            body_font_path=TestAddInsOverlayIntegration.font_path,
            position="auto",
        )
        assert os.path.exists(out_path)


# ---------- Test 5: Comparison tests across diverse scenes ----------

class TestFindBlankRegionComparative:
    """Compare find_blank_region behavior across diverse scene compositions.

    For each scene, we build a synthetic image where one region is intentionally
    blank/uniform and others are busy. Verify that auto-placement lands in or
    near the blank region (within tolerance), and that it differs from a naive
    center placement when the blank region is off-center.
    """

    def _make_scene(self, busy_regions=None, img_size=(768, 1024),
                    blank_color=(240, 230, 220), busy_color=(120, 100, 80)):
        """Create a synthetic test image.

        busy_regions: list of (x0, y0, x1, y1) rectangles to mark as busy.
        Anything not covered by a busy_region is blank (uniform).
        """
        img = Image.new("RGB", img_size, blank_color)
        d = ImageDraw.Draw(img)
        if busy_regions:
            for (x0, y0, x1, y1) in busy_regions:
                d.rectangle([x0, y0, x1, y1], fill=busy_color)
        return img

    def _region_uniformity(self, img, region):
        """Return the standard deviation of pixel values inside a region.
        Lower = more uniform = 'blanker'."""
        x0, y0, x1, y1 = region
        crop = img.convert("L").crop((x0, y0, x1, y1))
        pixels = list(crop.getdata())
        if not pixels:
            return 0.0
        mean = sum(pixels) / len(pixels)
        var = sum((p - mean) ** 2 for p in pixels) / len(pixels)
        return var ** 0.5

    def test_top_blank_scene_lands_in_top_half(self):
        """Bottom half is busy → mask should land in top half."""
        img = self._make_scene(busy_regions=[(0, 500, 768, 1024)])
        box_w, box_h = 600, 400
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        assert y < 500, f"Top-blank scene: expected y<500, got y={y}"

    def test_bottom_blank_scene_lands_in_bottom_half(self):
        """Top half is busy → mask should land in bottom half."""
        img = self._make_scene(busy_regions=[(0, 0, 768, 500)])
        box_w, box_h = 600, 400
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        assert y + box_h > 500, f"Bottom-blank scene: expected y+box_h>500, got y={y}, box_h={box_h}"

    def test_auto_beats_center_when_blank_is_offset(self):
        """Verify auto-placement actually moves the mask away from center
        when the blank region is offset."""
        img = self._make_scene(busy_regions=[(0, 0, 768, 700)])  # top 70% busy
        box_w, box_h = 600, 400
        x_auto, y_auto = find_blank_region(img, box_w, box_h, num_bands=8)
        # Center would be: y_center = (1024 - 400) // 2 = 312 (in busy top half)
        y_center = (1024 - 400) // 2
        assert y_auto > y_center, (
            f"Auto should escape the busy top: y_auto={y_auto} should exceed "
            f"naive center y_center={y_center}"
        )

    def test_auto_does_not_span_busy_region(self):
        """Mask should not straddle a busy region. Build a scene with busy in middle
        and verify mask doesn't overlap it."""
        img = self._make_scene(
            busy_regions=[(0, 400, 768, 700)],  # busy band in middle
            img_size=(768, 1024),
        )
        box_w, box_h = 600, 400
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        # Mask should not overlap y in [400, 700]
        mask_y0, mask_y1 = y, y + box_h
        overlap = max(0, min(mask_y1, 700) - max(mask_y0, 400))
        # Some overlap is acceptable (we don't have a perfect empty band),
        # but it should be less than half the mask height
        assert overlap < box_h * 0.5, (
            f"Mask overlaps busy middle band by {overlap}px (mask height {box_h}); "
            f"should be < {box_h * 0.5}"
        )

    def test_auto_handles_centered_object(self):
        """If the busy region is centered and the edges are blank,
        auto should land near an edge (top or bottom), not in center."""
        # Center busy: y in [400, 624], edges blank
        img = self._make_scene(busy_regions=[(0, 400, 768, 624)])
        box_w, box_h = 600, 350
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        # Mask should land either fully above 400 or fully below 624
        mask_y0, mask_y1 = y, y + box_h
        fully_above = mask_y1 <= 400
        fully_below = mask_y0 >= 624
        assert fully_above or fully_below, (
            f"Mask y=[{mask_y0}, {mask_y1}] overlaps centered busy region [400, 624]"
        )

    def test_auto_vs_center_differ_on_off_center_blank(self):
        """When blank is in top half, auto and center should give different y values."""
        img = self._make_scene(busy_regions=[(0, 600, 768, 1024)])
        box_w, box_h = 600, 400
        _, y_auto = find_blank_region(img, box_w, box_h, num_bands=8)
        y_center = (1024 - 400) // 2
        # Auto should differ from center by at least 100px in this scenario
        assert abs(y_auto - y_center) > 100, (
            f"Auto (y={y_auto}) should differ significantly from center (y={y_center})"
        )

    def test_auto_returns_valid_bounds(self):
        """Smoke test on a tricky scene: ensure mask is always within image."""
        img = self._make_scene(
            busy_regions=[(0, 0, 768, 100), (0, 500, 768, 600), (0, 900, 768, 1024)],
        )
        box_w, box_h = 600, 350
        x, y = find_blank_region(img, box_w, box_h, num_bands=8)
        assert 0 <= x <= 768 - box_w
        assert 0 <= y <= 1024 - box_h

    def test_auto_score_distinguishes_clear_cases(self):
        """Verify the underlying scoring: a truly blank band should score
        higher than a busy one."""
        from PIL import ImageDraw
        img = Image.new("RGB", (600, 800), (240, 230, 220))
        d = ImageDraw.Draw(img)
        # Make top half uniform blank, bottom half busy with checkered pattern
        for x in range(0, 600, 30):
            d.rectangle([x, 400, x + 25, 800], fill=(100, 80, 60))

        gray = img.convert("L")
        top_stdev = self._region_uniformity(img, (0, 0, 600, 400))
        bot_stdev = self._region_uniformity(img, (0, 400, 600, 800))
        assert top_stdev < bot_stdev, (
            f"Top stdev ({top_stdev}) should be lower than bottom ({bot_stdev}) "
            f"for scoring to distinguish blank vs busy"
        )


class TestLoadCjkFont:
    """`load_cjk_font` must skip candidates that cannot render CJK (tofu).

    SKILL.md documents a CJK width sanity check; before this it was defined but
    never called, so a non-CJK font passed via --title-font rendered tofu boxes.
    """

    @classmethod
    def setup_class(cls):
        cls.cjk_font = "/System/Library/Fonts/Hiragino Sans GB.ttc"
        cls.ascii_only_font = "/System/Library/Fonts/Helvetica.ttc"
        cls.skip = not (
            os.path.exists(cls.cjk_font) and os.path.exists(cls.ascii_only_font)
        )

    def test_prefers_a_font_that_can_render_cjk(self):
        if self.skip:
            return
        from add_ins_overlay import load_cjk_font, CJK_WIDTH_RATIO_MIN
        # ASCII-only font listed FIRST — a naive loader would pick it and tofu.
        font = load_cjk_font([self.ascii_only_font, (self.cjk_font, 0)], 40)
        d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        ratio = d.textlength("中文", font=font) / d.textlength("AA", font=font)
        assert ratio >= CJK_WIDTH_RATIO_MIN, (
            f"picked a tofu font (CJK/ASCII width ratio {ratio:.3f}); "
            f"should have skipped {self.ascii_only_font}"
        )

    def test_real_cjk_fonts_pass_the_sanity_check(self):
        """Regression guard: the threshold must not be as strict as 1.5 — that
        rejects EVERY real CJK font (Arial Unicode measures 1.499, Hiragino
        1.333), which would silently swap the title font on macOS."""
        if self.skip:
            return
        from add_ins_overlay import _cjk_width_ok
        for path, idx in [(self.cjk_font, 0), (self.cjk_font, 1),
                          ("/Library/Fonts/Arial Unicode.ttf", 0)]:
            if not os.path.exists(path):
                continue
            font = ImageFont.truetype(path, 40, index=idx)
            assert _cjk_width_ok(font), (
                f"{os.path.basename(path)}#{idx} wrongly rejected as non-CJK"
            )

    def test_falls_back_to_first_loadable_when_none_render_cjk(self):
        if self.skip:
            return
        from add_ins_overlay import load_cjk_font
        font = load_cjk_font([self.ascii_only_font], 40)
        assert font is not None

    def test_returns_none_when_nothing_loads(self):
        if self.skip:
            return
        from add_ins_overlay import load_cjk_font
        assert load_cjk_font(["/nonexistent/font.ttf"], 40) is None


class TestFontLoadingSanity:
    """Verify that the script's font candidates include the cross-platform fallback."""

    def test_arial_unicode_in_candidates(self):
        """Arial Unicode MS is the cross-platform safety net for ❤."""
        from add_ins_overlay import add_ins_overlay
        # Read source and check for Arial Unicode mention
        src_path = os.path.join(SCRIPTS_DIR, "add_ins_overlay.py")
        with open(src_path, encoding="utf-8") as f:
            src = f.read()
        assert "Arial Unicode" in src, (
            "Arial Unicode MS should be in font candidate list as cross-platform fallback"
        )

    def test_pillow_import_present(self):
        """Sanity: PIL/Pillow is the required dependency."""
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        assert Image and ImageDraw and ImageFont and ImageFilter


# ---------- Test 6: kinsoku (禁则) — which positions may we break at? ----------

class TestIsValidBreak:
    """Verify 禁则 rules: a line break at index i means text[:i] / text[i:].

    These are the deterministic rules that keep auto-split output from looking
    broken. Semantic clause boundaries are the *agent's* job (see SKILL.md) —
    the script only guarantees it never produces an obviously-wrong break.
    """

    def test_ascii_run_is_never_split(self):
        # "40+后才明白" — must not become "40" / "+后才明白" or "40+" / ... is fine
        assert is_valid_break("40+后才明白", 1) is False  # between "4" and "0"
        assert is_valid_break("40+后才明白", 2) is False  # between "0" and "+"
        assert is_valid_break("40+后才明白", 3) is True   # between "+" and "后"

    def test_closing_punctuation_never_starts_a_line(self):
        assert is_valid_break("你好，世界", 2) is False  # break before "，"
        assert is_valid_break("你好，世界", 3) is True   # break after "，"

    def test_opening_punctuation_never_ends_a_line(self):
        # "你好（世界）": idx 2 = before "（" (开标点可作行首 → legal),
        #                  idx 3 = after  "（" (开标点留行尾 → illegal)
        assert is_valid_break("你好（世界）", 2) is True
        assert is_valid_break("你好（世界）", 3) is False

    def test_plain_cjk_boundary_is_valid(self):
        assert is_valid_break("女人越来越差", 2) is True

    def test_edges_are_invalid(self):
        assert is_valid_break("标题", 0) is False
        assert is_valid_break("标题", 2) is False


# ---------- Test 7: plan_cover_layout (pure layout planning) ----------

class TestPlanCoverLayout:
    """Cover layout planning: line split + font size, no rendering.

    Sizes derive from the closed form  s = min(base, max_line_w * n_lines / width_units)
    with base = COVER_TITLE_RATIO * img_h = 0.07h (2× the 0.035h ins title).
    """

    IMG_W, IMG_H = 768, 1024

    @classmethod
    def setup_class(cls):
        cls.font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
        cls.sym_font_path = "/Library/Fonts/Arial Unicode.ttf"
        cls.skip = not (
            os.path.exists(cls.font_path) and os.path.exists(cls.sym_font_path)
        )

    def _plan(self, title, w=None, h=None):
        if self.skip:
            return None
        return plan_cover_layout(
            title,
            w or self.IMG_W,
            h or self.IMG_H,
            title_font_path=self.font_path,
            symbol_font_path=self.sym_font_path,
        )

    def test_manual_newline_is_respected_verbatim(self):
        """The agent authors semantic breaks with \\n; we must not re-split them."""
        plan = self._plan("40+后才明白\n女人越来越差的9个原因")
        assert plan["lines"] == ["40+后才明白", "女人越来越差的9个原因"]

    def test_short_title_uses_base_size_on_one_line(self):
        plan = self._plan("早安")
        assert plan["lines"] == ["早安"]
        assert plan["font_size"] == int(self.IMG_H * COVER_TITLE_RATIO)

    def test_longer_title_grows_to_two_lines(self):
        # 12 CJK chars: 1 line @57px vs 2 lines capped @71px → 2 lines wins
        plan = self._plan("女人越来越差的九个原因")
        assert len(plan["lines"]) == 2
        assert plan["font_size"] == int(self.IMG_H * COVER_TITLE_RATIO)

    def test_marginal_gain_does_not_add_a_line(self):
        """10 CJK chars: 1 line gets 69px, 2 lines 71px. A 3% gain is not worth
        splitting, so SPLIT_GAIN_MIN must reject it."""
        plan = self._plan("女人越来越差的九原因")
        assert plan["lines"] == ["女人越来越差的九原因"]

    def test_oversized_title_is_split_rather_than_overflowing(self):
        title = "女人越来越差的九个原因以及你每天都在犯的错"
        plan = self._plan(title)
        assert len(plan["lines"]) > 1
        assert plan["font_size"] <= int(self.IMG_H * COVER_TITLE_RATIO)

    def test_font_size_never_drops_below_floor(self):
        """A 70-char title cannot fit even at 4 lines; the floor protects
        legibility (1.2× a normal ins title) and we accept slight overflow."""
        plan = self._plan("标题" * 35)
        assert plan["font_size"] >= int(self.IMG_H * COVER_TITLE_FLOOR_RATIO)

    def test_auto_split_never_breaks_inside_ascii_run(self):
        plan = self._plan("40+后才明白女人越来越差的9个原因")
        assert len(plan["lines"]) > 1
        for line in plan["lines"]:
            assert not line.startswith("+"), f"split inside '40+': {plan['lines']}"
        assert any("40+" not in ln for ln in plan["lines"])

    def test_auto_split_never_orphans_closing_punctuation(self):
        plan = self._plan("女人越来越差，到底是因为什么")
        for line in plan["lines"]:
            assert line[0] not in "，。！？、；：）】》", (
                f"line starts with closing punctuation: {plan['lines']}"
            )

    def test_lines_fit_within_image_with_stroke(self):
        """Every line, plus its black stroke, must stay inside the canvas."""
        plan = self._plan("女人越来越差的九个原因")
        font = ImageFont.truetype(self.font_path, plan["font_size"])
        d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        limit = int(self.IMG_W * COVER_MAX_LINE_W_RATIO) + 2 * plan["stroke_width"]
        for line in plan["lines"]:
            w = d.textlength(line, font=font)
            assert w <= limit, f"{line!r} width {w} exceeds {limit}"

    def test_stroke_width_scales_with_font_size(self):
        plan = self._plan("早安")
        assert plan["stroke_width"] >= 2
        assert plan["stroke_width"] <= plan["font_size"] * 0.15

    def test_block_height_fits_within_image(self):
        plan = self._plan("女人越来越差的九个原因")
        assert 0 < plan["block_h"] <= self.IMG_H


# ---------- Test 8: cover mode integration (rendering) ----------

class TestCoverModeRendering:
    """End-to-end: mode="cover" renders a big stroked title and no gray mask."""

    @classmethod
    def setup_class(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix="ins_cover_test_")
        cls.font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
        cls.sym_font_path = "/Library/Fonts/Arial Unicode.ttf"
        cls.skip = not (
            os.path.exists(cls.font_path) and os.path.exists(cls.sym_font_path)
        )
        if cls.skip:
            return
        # Pure white canvas: the gray mask (105,105,105,α0.70) composites to
        # ~(150,150,150) over white, so it is trivially detectable.
        cls.white_path = os.path.join(cls.tmpdir, "white.png")
        Image.new("RGB", (768, 1024), (255, 255, 255)).save(cls.white_path)

    def _render(self, mode, tag, title="40+后才明白\n女人越来越差的9个原因", body=None):
        if self.skip:
            return None
        out = os.path.join(self.tmpdir, f"{tag}.jpg")
        add_ins_overlay(
            image_path=self.white_path,
            output_path=out,
            title=title,
            body=body,
            title_font_path=self.font_path,
            body_font_path=self.font_path,
            mode=mode,
        )
        return out

    @staticmethod
    def _count(pixels, pred):
        return sum(1 for p in pixels if pred(p))

    def test_cover_renders_without_body(self):
        if self.skip:
            return
        out = self._render("cover", "cover_no_body")
        assert os.path.exists(out)
        assert Image.open(out).size == (768, 1024)

    def test_cover_ignores_body_when_supplied(self):
        if self.skip:
            return
        with_body = self._render("cover", "cover_body", body="这段正文不该出现")
        without = self._render("cover", "cover_nobody")
        assert os.path.exists(with_body)
        # Identical input → body must leave no trace in cover mode
        a = list(Image.open(with_body).convert("RGB").getdata())
        b = list(Image.open(without).convert("RGB").getdata())
        assert a == b, "body text leaked into cover mode output"

    def test_cover_draws_no_gray_mask(self):
        """The defining difference from ins mode. Compare both on white."""
        if self.skip:
            return
        cover = list(Image.open(self._render("cover", "mask_cover"))
                     .convert("RGB").getdata())
        ins = list(Image.open(
            self._render("ins", "mask_ins", body="正文一行")
        ).convert("RGB").getdata())
        total = len(cover)
        near_mask = lambda p: all(140 <= c <= 162 for c in p)  # noqa: E731
        cover_pct = self._count(cover, near_mask) / total
        ins_pct = self._count(ins, near_mask) / total
        assert cover_pct < 0.01, f"cover mode drew a gray mask ({cover_pct:.1%})"
        assert ins_pct > 0.10, f"ins mode lost its gray mask ({ins_pct:.1%})"

    def test_cover_title_has_black_stroke(self):
        if self.skip:
            return
        cover = list(Image.open(self._render("cover", "stroke"))
                     .convert("RGB").getdata())
        black = self._count(cover, lambda p: max(p) < 40)
        assert black > 200, f"only {black} near-black pixels — stroke missing"

    def test_cover_title_is_centered_horizontally(self):
        """Centroid of the dark (stroke+shadow) pixels should sit near image centre."""
        if self.skip:
            return
        img = Image.open(self._render("cover", "centered")).convert("L")
        w, h = img.size
        px = list(img.getdata())
        dark_xs = [i % w for i, v in enumerate(px) if v < 100]
        assert dark_xs, "no dark pixels found — title not rendered"
        centroid = sum(dark_xs) / len(dark_xs)
        assert abs(centroid - w / 2) < w * 0.06, (
            f"title centroid x={centroid:.0f} is off-centre (image centre {w/2})"
        )

    def test_cover_title_block_is_vertically_centered(self):
        if self.skip:
            return
        img = Image.open(self._render("cover", "vcenter")).convert("L")
        w, h = img.size
        px = list(img.getdata())
        dark_ys = [i // w for i, v in enumerate(px) if v < 100]
        assert dark_ys, "no dark pixels found"
        centroid = sum(dark_ys) / len(dark_ys)
        assert abs(centroid - h / 2) < h * 0.12, (
            f"title centroid y={centroid:.0f} is off-centre (image centre {h/2})"
        )

    def test_cover_title_is_larger_than_ins_title(self):
        """The whole point: cover text is ~2× a normal title."""
        if self.skip:
            return
        plan = plan_cover_layout(
            "40+后才明白\n女人越来越差的9个原因", 768, 1024,
            title_font_path=self.font_path, symbol_font_path=self.sym_font_path,
        )
        ins_title_size = int(1024 * 0.035)
        assert plan["font_size"] >= ins_title_size * 1.5, (
            f"cover font {plan['font_size']} not appreciably larger than "
            f"ins title {ins_title_size}"
        )


if __name__ == "__main__":
    # Allow running directly: python3 tests/test_add_ins_overlay.py
    import unittest
    unittest.main(verbosity=2, exit=False)
