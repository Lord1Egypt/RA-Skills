from pathlib import Path

import pytest


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def color_system_page(page):
    url = f"file://{FIXTURES_DIR / 'color_system_report.html'}"
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")
    return page


def badge_signature(page, selector: str) -> str:
    return page.eval_on_selector(
        selector,
        """el => {
            const s = getComputedStyle(el);
            return `${s.backgroundColor}|${s.color}|${s.borderColor}`;
        }""",
    )


def test_default_badges_share_one_neutral_palette(color_system_page):
    signatures = color_system_page.evaluate(
        """() => ['blue', 'green', 'purple', 'orange', 'red', 'teal', 'done'].map(name => {
            const el = document.querySelector(`#default .badge--${name}`);
            const s = getComputedStyle(el);
            return `${s.backgroundColor}|${s.color}|${s.borderColor}`;
        })"""
    )
    assert len(set(signatures)) == 1


def test_warn_and_err_keep_semantic_difference(color_system_page):
    warn_sig = badge_signature(color_system_page, "#default .badge--warn")
    err_sig = badge_signature(color_system_page, "#default .badge--err")
    done_sig = badge_signature(color_system_page, "#default .badge--done")
    assert warn_sig != done_sig
    assert err_sig != done_sig
    assert warn_sig != err_sig


def test_default_kpi_accent_attributes_do_not_reintroduce_rainbow(color_system_page):
    signatures = color_system_page.evaluate(
        """() => Array.from(document.querySelectorAll('#default .kpi-card')).map(card => {
            const cardStyle = getComputedStyle(card);
            const valueStyle = getComputedStyle(card.querySelector('.kpi-value'));
            return `${cardStyle.borderTopColor}|${valueStyle.color}`;
        })"""
    )
    assert len(set(signatures)) == 1


def test_comparison_mode_only_entity_badges_diverge(color_system_page):
    entity_signatures = color_system_page.evaluate(
        """() => ['a', 'b', 'c'].map(name => {
            const el = document.querySelector(`#comparison .badge--entity-${name}`);
            const s = getComputedStyle(el);
            return `${s.backgroundColor}|${s.color}|${s.borderColor}`;
        })"""
    )
    neutral_signature = badge_signature(color_system_page, "#comparison .badge--blue")
    assert len(set(entity_signatures)) == 3
    assert neutral_signature not in entity_signatures
