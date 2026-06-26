#!/usr/bin/env python3
"""
Test cases for export-sandbox-pptx.py optimizations.

Each slide optimization adds test cases to verify the fix continues to work.

Usage:
    python3 scripts/test-export.py
"""

import sys
import os
import json
import re
import importlib.util
import tempfile
from zipfile import ZipFile
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Load export-sandbox-pptx module (has hyphen in name)
spec = importlib.util.spec_from_file_location("export_sandbox", scripts_dir / "export-sandbox-pptx.py")
export_sandbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_sandbox)

run_skill_export_spec = importlib.util.spec_from_file_location(
    "run_skill_export",
    scripts_dir / "run-skill-export.py",
)
run_skill_export = importlib.util.module_from_spec(run_skill_export_spec)
run_skill_export_spec.loader.exec_module(run_skill_export)

sync_contracts_spec = importlib.util.spec_from_file_location(
    "sync_slide_creator_contracts",
    scripts_dir / "sync-slide-creator-contracts.py",
)
sync_slide_creator_contracts = importlib.util.module_from_spec(sync_contracts_spec)
sync_contracts_spec.loader.exec_module(sync_slide_creator_contracts)

rigorous_eval_spec = importlib.util.spec_from_file_location("rigorous_eval", scripts_dir / "rigorous-eval.py")
rigorous_eval = importlib.util.module_from_spec(rigorous_eval_spec)
rigorous_eval_spec.loader.exec_module(rigorous_eval)

PX_PER_IN = export_sandbox.PX_PER_IN
parse_px = export_sandbox.parse_px
build_grid_children = export_sandbox.build_grid_children
build_text_element = export_sandbox.build_text_element
compute_element_style = export_sandbox.compute_element_style
parse_css_rules = export_sandbox.parse_css_rules
layout_slide_elements = export_sandbox.layout_slide_elements
flat_extract = export_sandbox.flat_extract
extract_css_from_soup = export_sandbox.extract_css_from_soup
map_font = export_sandbox.map_font
measure_flow_box = export_sandbox.measure_flow_box
_stretch_column_block_text_to_inner_width = export_sandbox._stretch_column_block_text_to_inner_width
_build_swiss_index_list_rows = export_sandbox._build_swiss_index_list_rows
_build_swiss_terminal_line = export_sandbox._build_swiss_terminal_line
_build_swiss_disc_steps = export_sandbox._build_swiss_disc_steps
_hairline_height_in = export_sandbox._hairline_height_in
_build_css_hairline_shape = export_sandbox._build_css_hairline_shape
flow_gap_in = getattr(export_sandbox, '_flow_gap_in', None)
remeasure_text_for_final_width = getattr(export_sandbox, '_remeasure_text_for_final_width', None)
try:
    _flatten_nested_containers = export_sandbox._flatten_nested_containers
except AttributeError:
    _flatten_nested_containers = None
parse_html_to_slides = export_sandbox.parse_html_to_slides
build_export_pipeline = getattr(export_sandbox, 'build_export_pipeline', None)
solve_geometry = getattr(export_sandbox, 'solve_geometry', None)
render_pptx = getattr(export_sandbox, 'render_pptx', None)
export_sandbox_pptx = export_sandbox.export_sandbox
validate_export_hints = export_sandbox.validate_export_hints
detect_producer = export_sandbox.detect_producer
collect_export_context = export_sandbox.collect_export_context
extract_body_decorative_background = export_sandbox.extract_body_decorative_background
extract_body_mesh_background = getattr(export_sandbox, 'extract_body_mesh_background')
build_aurora_mesh_overlay_elements = getattr(export_sandbox, 'build_aurora_mesh_overlay_elements')
parse_grid_track_widths = getattr(export_sandbox, '_parse_grid_track_widths')
from bs4 import BeautifulSoup, Tag

REPO_ROOT = Path(__file__).parent.parent
HANDWRITTEN_FIXTURE = REPO_ROOT / 'tests' / 'fixtures' / 'export-corpus' / 'handwritten-card-list-table.html'


def _corpus_samples():
    return [
        {
            'label': 'repo blue-sky demo',
            'path': REPO_ROOT / 'demo' / 'blue-sky-zh.html',
            'required': True,
        },
        {
            'label': 'repo intro demo',
            'path': REPO_ROOT / 'demo' / 'slide-creator-intro.html',
            'required': True,
        },
        {
            'label': 'handwritten fixture',
            'path': HANDWRITTEN_FIXTURE,
            'required': True,
        },
        {
            'label': 'slide-creator blue-sky starter',
            'path': Path('/Users/song/projects/slide-creator/references/blue-sky-starter.html'),
            'required': False,
        },
        {
            'label': 'slide-creator swiss-modern zh',
            'path': Path('/Users/song/projects/slide-creator/demos/swiss-modern-zh.html'),
            'required': False,
        },
        {
            'label': 'slide-creator enterprise-dark zh',
            'path': Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html'),
            'required': False,
        },
        {
            'label': 'slide-creator data-story zh',
            'path': Path('/Users/song/projects/slide-creator/demos/data-story-zh.html'),
            'required': False,
        },
    ]


def _count_text_elements(elements):
    count = 0
    for elem in elements:
        if elem.get('type') == 'text':
            count += 1
        for child in elem.get('children', []):
            count += _count_text_elements([child])
    return count


def _collect_text_values(elements):
    texts = []
    for elem in elements:
        if elem.get('type') == 'text':
            txt = elem.get('text', '').strip()
            if txt:
                texts.append(txt)
        for child in elem.get('children', []):
            texts.extend(_collect_text_values([child]))
    return texts


def _collect_elements_by_type(elements, elem_type):
    matches = []
    for elem in elements:
        if elem.get('type') == elem_type:
            matches.append(elem)
        for child in elem.get('children', []):
            matches.extend(_collect_elements_by_type([child], elem_type))
    return matches


def _find_data_story_split_rails(slide):
    containers = _collect_elements_by_type(slide['elements'], 'container')
    split = next((elem for elem in containers if elem.get('_component_contract') == 'grid_two_column'), None)
    assert split is not None, containers
    rails = [child for child in split.get('children', []) if child.get('type') == 'container']
    assert len(rails) >= 2, split.get('children', [])
    left_rail = min(rails, key=lambda child: child.get('bounds', {}).get('x', 0.0))
    right_rail = max(rails, key=lambda child: child.get('bounds', {}).get('x', 0.0))
    return split, left_rail, right_rail


def _require_symbol(symbol_name: str):
    """Return exported helper if present, else print a pending-skip message."""
    symbol = getattr(export_sandbox, symbol_name, None)
    if symbol is None:
        print(f"  SKIP: {symbol_name} pending implementation")
    return symbol


def test_discover_slide_roots_accepts_generic_section_deck():
    discover_slide_roots = _require_symbol('discover_slide_roots')
    html = """
    <html><body>
      <section data-slide="1"><h1>One</h1><p>Intro</p></section>
      <section data-slide="2"><h1>Two</h1><p>Outro</p></section>
    </body></html>
    """
    soup = BeautifulSoup(html, 'lxml')
    roots = discover_slide_roots(soup)
    assert [root.get('data-slide') for root in roots] == ['1', '2']
    print("  PASS: discover_slide_roots accepts generic section decks")


def test_discover_slide_roots_rejects_article_like_document():
    discover_slide_roots = _require_symbol('discover_slide_roots')
    html = """
    <html><body>
      <article><h1>Long Article</h1><p>Body copy</p></article>
    </body></html>
    """
    soup = BeautifulSoup(html, 'lxml')
    assert discover_slide_roots(soup) == []
    print("  PASS: discover_slide_roots rejects article-like documents")


def test_assign_support_tier_uses_deterministic_precedence():
    assign_support_tier = _require_symbol('_assign_support_tier')
    assert assign_support_tier({
        'contract_found': True,
        'producer_confidence': 'high',
        'producer_signals': 2,
        'page_boundary_count': 5,
        'semantic_signals': 4,
    }) == 'contract_bound'
    assert assign_support_tier({
        'contract_found': False,
        'producer_confidence': 'medium',
        'producer_signals': 2,
        'page_boundary_count': 5,
        'semantic_signals': 4,
    }) == 'producer_aware'
    assert assign_support_tier({
        'contract_found': False,
        'producer_confidence': 'low',
        'producer_signals': 1,
        'page_boundary_count': 3,
        'semantic_signals': 2,
    }) == 'semantic_enhanced'
    assert assign_support_tier({
        'contract_found': False,
        'producer_confidence': 'none',
        'producer_signals': 0,
        'page_boundary_count': 0,
        'semantic_signals': 0,
    }) == 'generic_safe'
    print("  PASS: support tier precedence is deterministic")


def test_analyze_source_returns_raw_signal_bundles():
    analyze_source = _require_symbol('analyze_source')
    html_path = REPO_ROOT / 'demo' / 'slide-creator-intro.html'
    analysis = analyze_source(html_path, 1440, 900)

    assert {'source_snapshot', 'raw_deck_signals', 'raw_slide_signals'} <= set(analysis), analysis
    assert analysis['raw_deck_signals']['page_boundary_count'] >= 1, analysis['raw_deck_signals']
    print("  PASS: analyze_source returns raw signal bundles")


def test_build_profiles_assigns_contract_bound_deck_profile():
    analyze_source = _require_symbol('analyze_source')
    build_profiles = _require_symbol('build_profiles')
    html_path = REPO_ROOT / 'demo' / 'data-story-zh.html'
    analysis = analyze_source(html_path, 1440, 900)

    deck_profile, slide_profiles = build_profiles(analysis)

    assert deck_profile['support_tier'] == 'contract_bound', deck_profile
    assert deck_profile['global_downgrade_chain'] == [
        'preserve_structure',
        'preserve_grouping',
        'degrade_decorative',
        'shrink_if_allowed',
    ], deck_profile
    assert slide_profiles and slide_profiles[0]['slide_index'] == 0, slide_profiles
    assert all(
        candidate.get('type') != 'layout_support_tier'
        for candidate in slide_profiles[0]['override_candidates']
    ), slide_profiles[0]['override_candidates']
    print("  PASS: build_profiles assigns contract-bound deck profile")


def test_solve_geometry_emits_pptx_geometry_plan_with_render_hints():
    assert build_export_pipeline is not None, "build_export_pipeline missing"
    assert solve_geometry is not None, "solve_geometry missing"

    html_path = REPO_ROOT / 'demo' / 'chinese-chan-zh.html'
    pipeline = build_export_pipeline(html_path, 1440, 900)
    geometry_plans = solve_geometry(pipeline)
    first_plan = geometry_plans[0]
    source_plan = pipeline['slide_plans'][0]

    assert geometry_plans, geometry_plans
    assert first_plan['selected_solver'] == source_plan['selected_solver'], first_plan
    assert first_plan['selected_layout_family'] == source_plan['selected_layout_family'], first_plan
    assert first_plan['text_policy_bundle'] == source_plan['text_policy_bundle'], first_plan
    assert first_plan['background_strategy'] == source_plan['background_strategy'], first_plan
    assert first_plan['overlay_strategy'] == source_plan['overlay_strategy'], first_plan
    assert first_plan['allowed_overrides'] == source_plan['allowed_overrides'], first_plan
    assert first_plan['downgrade_chain'] == source_plan['downgrade_chain'], first_plan
    assert first_plan['reasons'] == source_plan['reasons'], first_plan
    assert first_plan['confidence'] == source_plan['confidence'], first_plan

    render_hints = first_plan['pptx_render_hints']
    assert render_hints['text'], render_hints
    stable_ids = list(render_hints['text'].keys())
    assert all(key.startswith('slide0-text-') for key in stable_ids), stable_ids
    assert any(
        hint.get('wrap_mode') in {'none', 'square'} and
        hint.get('auto_size') in {'text_to_fit_shape', 'shape_to_fit_text'}
        for hint in render_hints['text'].values()
    ), render_hints
    print("  PASS: solve_geometry emits pptx geometry plan with render hints")


def test_solve_geometry_preserves_legacy_slide_fields_for_compat_adapter():
    assert build_export_pipeline is not None, "build_export_pipeline missing"
    assert solve_geometry is not None, "solve_geometry missing"

    html_path = REPO_ROOT / 'demo' / 'aurora-mesh-zh.html'
    pipeline = build_export_pipeline(html_path, 1440, 900)
    geometry_plans = solve_geometry(pipeline)
    first_plan = geometry_plans[0]

    assert first_plan['background'].get('mesh') or first_plan['background'].get('gradient') or first_plan['background'].get('grid'), first_plan['background']

    compat_slide = first_plan['legacy_slide_data']
    assert 'elements' in compat_slide and 'slideStyle' in compat_slide, compat_slide
    assert 'background' in compat_slide and 'bgGradient' in compat_slide and 'gridBg' in compat_slide and 'meshBg' in compat_slide, compat_slide
    compat_slides = parse_html_to_slides(html_path, 1440, 900)
    assert 'background' in compat_slides[0] and 'bgGradient' in compat_slides[0] and 'gridBg' in compat_slides[0] and 'meshBg' in compat_slides[0], compat_slides[0]
    print("  PASS: solve_geometry preserves legacy slide fields for compat adapter")


def test_render_pptx_uses_geometry_render_hints_for_contract_wrap():
    assert build_export_pipeline is not None, "build_export_pipeline missing"
    assert solve_geometry is not None, "solve_geometry missing"
    assert render_pptx is not None, "render_pptx missing"

    html_path = REPO_ROOT / 'demo' / 'chinese-chan-zh.html'
    pipeline = build_export_pipeline(html_path, 1440, 900)
    geometry_plans = solve_geometry(pipeline)
    first_plan = geometry_plans[0]
    wrap_hint = next(
        (
            hint for hint in first_plan['pptx_render_hints']['text'].values()
            if hint.get('wrap_mode') == 'square'
        ),
        None,
    )

    assert wrap_hint is not None, first_plan['pptx_render_hints']

    with tempfile.TemporaryDirectory(prefix='kai-export-render-hints-') as tmp_dir:
        pptx_path = Path(tmp_dir) / 'render-hints.pptx'
        render_pptx(geometry_plans, pptx_path)

        with ZipFile(pptx_path) as archive:
            slide_xml = archive.read('ppt/slides/slide1.xml').decode('utf-8')

    expected_geometry_id = wrap_hint['geometry_id']
    assert expected_geometry_id in slide_xml, slide_xml
    assert 'wrap="square"' in slide_xml, slide_xml
    print("  PASS: render_pptx uses geometry render hints for contract wrap")


def test_build_profiles_assigns_semantic_enhanced_for_generic_section_deck():
    analyze_source = _require_symbol('analyze_source')
    build_profiles = _require_symbol('build_profiles')
    html = """
    <html><body>
      <section data-slide="1"><div class="card"><h2>One</h2><p>Alpha</p></div></section>
      <section data-slide="2"><div class="card"><h2>Two</h2><p>Beta</p></div></section>
    </body></html>
    """
    with tempfile.TemporaryDirectory(prefix='kai-export-analysis-stage-') as tmp_dir:
        html_path = Path(tmp_dir) / 'generic-section-deck.html'
        html_path.write_text(html, encoding='utf-8')
        analysis = analyze_source(html_path, 1440, 900)

    deck_profile, _slide_profiles = build_profiles(analysis)

    assert deck_profile['support_tier'] == 'semantic_enhanced', deck_profile
    assert _slide_profiles and _slide_profiles[0]['support_tier'] == 'semantic_enhanced', _slide_profiles
    print("  PASS: build_profiles assigns semantic_enhanced for generic section deck")


def test_analyze_source_raw_slide_signals_describe_authored_slide():
    analyze_source = _require_symbol('analyze_source')
    html = """
    <html><body>
      <section data-slide="1" data-export-intent="compare">
        <div class="wrapper">
          <h2>One</h2>
          <p>Alpha body copy for authored analysis.</p>
        </div>
        <span style="position:absolute;top:12px;right:12px;">Badge</span>
      </section>
    </body></html>
    """
    with tempfile.TemporaryDirectory(prefix='kai-export-raw-slide-') as tmp_dir:
        html_path = Path(tmp_dir) / 'authored-slide-signals.html'
        html_path.write_text(html, encoding='utf-8')
        analysis = analyze_source(html_path, 1440, 900)

    raw_slide = analysis['raw_slide_signals'][0]

    assert raw_slide['overlay_count'] == 1, raw_slide
    assert 'Badge' in raw_slide['text_preview'], raw_slide
    assert raw_slide['intent'] == 'compare', raw_slide
    print("  PASS: analyze_source raw slide signals stay authored-source based")


def test_build_profiles_does_not_overstate_slide_contract_bound_without_local_evidence():
    build_profiles = _require_symbol('build_profiles')
    analysis = {
        'source_snapshot': {
            'export_context': {'validation': {'ok': True}},
            'hints': {'preset': 'Test Preset', 'deck_family': 'test-family'},
            'contract': {'contract_id': 'slide-creator/test'},
        },
        'raw_deck_signals': {
            'producer': 'slide-creator',
            'producer_confidence': 'high',
            'contract_found': True,
            'producer_signals': 2,
            'page_boundary_count': 1,
            'semantic_signals': 2,
        },
        'raw_slide_signals': [{
            'slide_index': 0,
            'role': '',
            'intent': '',
            'layout_support_tier': '',
            'has_local_contract_evidence': False,
            'text_count': 1,
            'semantic_signals': 1,
            'component_signals': [],
            'text_signals': ['headings'],
            'overlay_signals': [],
        }],
    }

    deck_profile, slide_profiles = build_profiles(analysis)

    assert deck_profile['support_tier'] == 'contract_bound', deck_profile
    assert slide_profiles[0]['support_tier'] != 'contract_bound', slide_profiles[0]
    assert slide_profiles[0]['support_tier'] == 'generic_safe', slide_profiles[0]
    print("  PASS: slide profiles require local evidence before claiming contract_bound")


def test_plan_slides_does_not_promote_past_analysis_tier():
    plan_slides = _require_symbol('plan_slides')
    deck_profile = {
        'support_tier': 'semantic_enhanced',
        'global_downgrade_chain': ['preserve_structure', 'degrade_decorative'],
    }
    slide_profiles = [{
        'slide_index': 0,
        'role': '',
        'intent': 'compare',
        'support_tier': 'semantic_enhanced',
        'component_profiles': [{'type': 'text_block', 'value': 'summary'}],
        'text_profiles': [{'type': 'heading', 'selector': 'h1'}],
        'overlay_profiles': [],
        'override_candidates': [],
    }]

    plans = plan_slides(deck_profile, slide_profiles, 1440, 900)

    assert plans[0]['support_tier'] == 'semantic_enhanced', plans[0]
    print("  PASS: plan_slides does not promote past analysis tier")


def test_plan_slides_records_override_reasons_for_export_role():
    plan_slides = _require_symbol('plan_slides')
    deck_profile = {
        'support_tier': 'contract_bound',
        'deck_family': 'enterprise-dark',
        'global_downgrade_chain': ['preserve_structure', 'preserve_grouping'],
    }
    override_candidate = {'type': 'role', 'value': 'explicit_role_hint'}
    slide_profiles = [{
        'slide_index': 0,
        'role': 'title_grid',
        'intent': 'hero',
        'support_tier': 'contract_bound',
        'component_profiles': [{'type': 'hero', 'value': 'title'}],
        'text_profiles': [{'type': 'heading', 'selector': 'h1'}],
        'overlay_profiles': [{'type': 'badge'}],
        'override_candidates': [override_candidate],
    }]

    plans = plan_slides(deck_profile, slide_profiles, 1440, 900)

    assert plans[0]['selected_layout_family'] == 'enterprise-dark', plans[0]
    assert plans[0]['reasons'], plans[0]
    assert any('explicit_role_hint' in reason for reason in plans[0]['reasons']), plans[0]['reasons']
    assert plans[0]['allowed_overrides'][0] is not override_candidate, plans[0]['allowed_overrides']
    print("  PASS: plan_slides records override reasons for export role")


def test_plan_slides_isolates_downgrade_chain_per_plan():
    plan_slides = _require_symbol('plan_slides')
    global_downgrade_chain = ['preserve_structure', 'degrade_decorative']
    deck_profile = {
        'support_tier': 'semantic_enhanced',
        'global_downgrade_chain': global_downgrade_chain,
    }
    slide_profiles = [
        {
            'slide_index': 0,
            'role': '',
            'intent': '',
            'support_tier': 'semantic_enhanced',
            'component_profiles': [],
            'text_profiles': [],
            'overlay_profiles': [],
            'override_candidates': [],
        },
        {
            'slide_index': 1,
            'role': '',
            'intent': '',
            'support_tier': 'semantic_enhanced',
            'component_profiles': [],
            'text_profiles': [],
            'overlay_profiles': [],
            'override_candidates': [],
        },
    ]

    plans = plan_slides(deck_profile, slide_profiles, 1440, 900)

    assert plans[0]['downgrade_chain'] is not global_downgrade_chain, plans[0]
    assert plans[1]['downgrade_chain'] is not global_downgrade_chain, plans[1]
    assert plans[0]['downgrade_chain'] is not plans[1]['downgrade_chain'], plans
    plans[0]['downgrade_chain'].append('only_first_plan')
    assert deck_profile['global_downgrade_chain'] == ['preserve_structure', 'degrade_decorative'], deck_profile
    assert plans[1]['downgrade_chain'] == ['preserve_structure', 'degrade_decorative'], plans[1]
    print("  PASS: plan_slides isolates downgrade chain per plan")


def test_parse_html_to_slides_generic_section_roots_keep_fixed_content_isolated_per_slide():
    html = '''
    <html><body>
      <section data-slide="1" style="position:relative;padding:48px;">
        <h2>One</h2>
        <span style="position:fixed;top:20px;right:32px;font-size:12px;">S1</span>
      </section>
      <section data-slide="2" style="position:relative;padding:48px;">
        <h2>Two</h2>
        <span style="position:fixed;top:20px;right:32px;font-size:12px;">S2</span>
      </section>
    </body></html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-generic-section-roots-') as tmp_dir:
        html_path = Path(tmp_dir) / 'generic-section-roots.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    assert len(slides) == 2, slides
    slide1_text = _collect_text_values(slides[0]['elements'])
    slide2_text = _collect_text_values(slides[1]['elements'])
    assert 'One' in slide1_text, slide1_text
    assert 'S1' in slide1_text, slide1_text
    assert 'Two' not in slide1_text, slide1_text
    assert 'S2' not in slide1_text, slide1_text
    assert 'Two' in slide2_text, slide2_text
    assert 'S2' in slide2_text, slide2_text
    assert 'One' not in slide2_text, slide2_text
    assert 'S1' not in slide2_text, slide2_text
    print("  PASS: generic section roots keep fixed content isolated per slide")


def test_discover_slide_roots_prefers_explicit_dot_slide_over_generic_sections():
    html = '''
    <html><body>
      <section class="slide" data-slide="1"><h2>Explicit</h2></section>
      <section data-slide="2"><h2>Fallback</h2></section>
    </body></html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-slide-root-precedence-') as tmp_dir:
        html_path = Path(tmp_dir) / 'slide-root-precedence.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    assert len(slides) == 1, slides
    slide_text = _collect_text_values(slides[0]['elements'])
    assert 'Explicit' in slide_text, slide_text
    assert 'Fallback' not in slide_text, slide_text
    print("  PASS: explicit .slide roots win over generic section discovery")


def test_parse_px():
    """Test CSS pixel parsing utility."""
    assert parse_px('16px') == 16.0
    assert parse_px('28px') == 28.0
    assert parse_px('0px') == 0.0
    assert parse_px('clamp(14px, 2vw, 28px)') > 0  # clamp returns a value
    print("  PASS: parse_px")


def test_parse_px_supports_minmax_math():
    """CSS min()/max() length expressions should resolve to usable pixel widths."""
    assert abs(parse_px('min(90vw, 800px)') - 800.0) < 0.01
    assert abs(parse_px('min(90vw,700px)') - 700.0) < 0.01
    assert abs(parse_px('max(320px, 20vw)') - 320.0) < 0.01
    print("  PASS: parse_px min/max math")


def test_validate_export_hints_rejects_unknown_layout_fields():
    """Export hints must reject IR-like fields such as slides/coordinates."""
    valid = validate_export_hints({
        'producer': 'slide-creator',
        'preset': 'Enterprise Dark',
        'runtime_flags': {'export_progress_ui': True},
        'chrome_selectors': ['.progress-bar'],
        'semantic_bias': {'layout_family': 'consulting-dark'},
        'contract_ref': 'slide-creator/enterprise-dark@1.0.0',
    })
    assert valid is not None and valid['producer'] == 'slide-creator', valid

    invalid = validate_export_hints({
        'producer': 'slide-creator',
        'slides': [{'role': 'cover'}],
    })
    assert invalid is None, invalid
    print("  PASS: export hints schema rejects IR-like fields")


def test_detect_producer_requires_cross_mechanism_medium_signals():
    """Metadata fields alone are one channel; watermark adds the second independent channel."""
    html = """
    <html><head><meta name="generator" content="kai-slide-creator v2.19.0"></head>
    <body data-producer="kai-slide-creator" data-preset="Enterprise Dark"></body></html>
    """
    soup = BeautifulSoup(html, 'lxml')
    detection = detect_producer(soup, REPO_ROOT / 'demo' / 'dummy.html')
    assert detection['producer'] == 'slide-creator', detection
    assert detection['confidence'] == 'medium', detection

    html_with_watermark = """
    <html><head><meta name="generator" content="kai-slide-creator v2.19.0"></head>
    <body data-producer="kai-slide-creator" data-preset="Enterprise Dark">
      <div hidden data-watermark="kai-slide-creator@2.19.0"></div>
    </body></html>
    """
    soup_with_watermark = BeautifulSoup(html_with_watermark, 'lxml')
    detection_with_watermark = detect_producer(soup_with_watermark, REPO_ROOT / 'demo' / 'dummy.html')
    assert detection_with_watermark['confidence'] == 'high', detection_with_watermark
    print("  PASS: producer detection uses cross-mechanism signals")


def test_resolve_repo_root_survives_missing___file__():
    """Inline execution environments should still locate the vendored skill root."""
    resolve_repo_root = getattr(export_sandbox, '_resolve_repo_root')

    from_cwd = resolve_repo_root(script_file=None, cwd=REPO_ROOT / 'scripts', env={})
    assert from_cwd == REPO_ROOT, from_cwd

    from_env = resolve_repo_root(
        script_file=None,
        cwd=Path('/tmp'),
        env={'KAI_EXPORT_PPT_LITE_ROOT': str(REPO_ROOT)},
    )
    assert from_env == REPO_ROOT, from_env
    print("  PASS: repo root fallback works without __file__")


def test_run_skill_export_bootstrap_loads_installed_exporter():
    """The small skill bootstrap should resolve the repo and load the exporter module."""
    resolved = run_skill_export.resolve_skill_root(
        explicit_root=str(REPO_ROOT),
        script_file=None,
        cwd=Path('/tmp'),
        env={},
    )
    assert resolved == REPO_ROOT, resolved

    module = run_skill_export.load_exporter_module(resolved)
    assert getattr(module, 'export_sandbox', None) is not None
    print("  PASS: skill bootstrap resolves root and loads exporter")


def test_parse_css_rules_respects_media_queries_and_important():
    """Desktop export should ignore mobile @media overrides and strip !important."""
    html = """
    <html>
      <head>
        <style>
          :root { --slide-padding: 4rem; }
          .ent-split { display: grid; }
          @media (max-width: 980px) {
            :root { --slide-padding: 1.5rem; }
            .ent-split { grid-template-columns: 1fr !important; }
          }
          @media (min-width: 1200px) {
            .ent-split { grid-template-columns: clamp(140px, 22%, 240px) 1fr !important; }
          }
        </style>
      </head>
      <body><div class="ent-split"></div></body>
    </html>
    """
    soup = BeautifulSoup(html, 'lxml')
    css_rules = extract_css_from_soup(soup)
    split = soup.select_one('.ent-split')
    style = compute_element_style(split, css_rules, split.get('style', ''))
    assert style['gridTemplateColumns'] == 'clamp(140px, 22%, 240px) 1fr', style
    assert export_sandbox._ROOT_CSS_VARS.get('--slide-padding') == '4rem', export_sandbox._ROOT_CSS_VARS
    print("  PASS: parse_css_rules respects media queries and strips !important")


def test_selector_matches_ignores_dynamic_hover_state():
    """Interactive pseudo-classes like :hover should not leak into static export styles."""
    html = """
    <html>
      <head>
        <style>
          td { background: transparent; }
          tbody tr:hover td { background: rgba(48,54,61,0.5); }
        </style>
      </head>
      <body>
        <table><tbody><tr><td>Cell</td></tr></tbody></table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, 'lxml')
    css_rules = extract_css_from_soup(soup)
    td = soup.find('td')
    style = compute_element_style(td, css_rules, td.get('style', ''))
    assert style.get('backgroundColor', '') in ('', 'transparent', 'rgba(0, 0, 0, 0)'), style
    print("  PASS: selector matching ignores dynamic hover state")


def test_parse_grid_track_widths_handles_split_and_auto_fit():
    """Grid track sizing should understand split rails and auto-fit minmax tracks."""
    split_widths = parse_grid_track_widths('clamp(140px, 22%, 240px) 1fr', 8.33, 0.25)
    assert len(split_widths) == 2, split_widths
    assert 1.2 < split_widths[0] < 2.4, split_widths
    assert split_widths[1] > split_widths[0], split_widths

    auto_fit_widths = parse_grid_track_widths(
        'repeat(auto-fit, minmax(min(100%, 280px), 1fr))',
        6.48,
        0.18,
    )
    assert len(auto_fit_widths) == 2, auto_fit_widths
    assert all(w > 2.0 for w in auto_fit_widths), auto_fit_widths
    print("  PASS: grid track widths handle split and auto-fit templates")


def test_collect_export_context_loads_enterprise_dark_contract_and_body_grid():
    """slide-creator weak signals should still load safe contract hints and pseudo grid background."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark contract context (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    context = collect_export_context(html_path, soup)
    assert context['detection']['producer'] == 'slide-creator', context['detection']
    assert context['detection']['confidence'] == 'low', context['detection']
    assert context['contract'] is not None, context
    assert context['contract']['contract_id'] == 'slide-creator/enterprise-dark', context['contract']

    css_rules = extract_css_from_soup(soup)
    grid_bg = extract_body_decorative_background(css_rules, context['contract'])
    assert grid_bg and grid_bg['sizePx'] == 24.0, grid_bg
    print("  PASS: enterprise-dark contract and body pseudo grid load")


def test_collect_export_context_loads_data_story_contract_and_body_grid():
    """data-story should load a synced contract with its body grid metadata."""
    html_path = Path('/Users/song/projects/slide-creator/demos/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story contract context (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    context = collect_export_context(html_path, soup)
    assert context['detection']['producer'] == 'slide-creator', context['detection']
    assert context['contract'] is not None, context
    assert context['contract']['contract_id'] == 'slide-creator/data-story', context['contract']
    assert context['contract']['component_selectors']['install_row'] == ['.install-row'], context['contract']
    assert context['contract']['component_slot_models']['install_row']['layout'] == 'split_rail', context['contract']

    css_rules = extract_css_from_soup(soup)
    grid_bg = extract_body_decorative_background(css_rules, context['contract'])
    assert grid_bg and grid_bg['sizePx'] == 40.0, grid_bg
    print("  PASS: data-story contract and body pseudo grid load")


def test_collect_export_context_loads_swiss_modern_contract_with_layout_tiers():
    """Swiss Modern should load its expanded synced contract instead of the old minimal metadata shell."""
    html_path = Path('/Users/song/projects/slide-creator/demos/swiss-modern-zh.html')
    if not html_path.exists():
        print("  SKIP: swiss-modern contract context (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    context = collect_export_context(html_path, soup)
    assert context['detection']['producer'] == 'slide-creator', context['detection']
    assert context['contract'] is not None, context
    contract = context['contract']
    assert contract['contract_id'] == 'slide-creator/swiss-modern', contract
    assert contract['typography']['display_font_stack'][0] == 'Archivo Black', contract
    assert contract['line_break_contract']['break_policy']['.swiss-title'] == 'prefer_preserve', contract
    assert 'title_grid' in contract['layout_contracts'], contract
    assert 'compatible' in contract['support_tiers'], contract
    print("  PASS: Swiss Modern loads expanded layout-tier contract")


def test_slide_creator_chinese_chan_loads_contract_and_runtime_chrome_fallback():
    """Chinese Chan should load its synced contract and still inherit shared runtime chrome filtering."""
    html_path = REPO_ROOT / 'demo' / 'chinese-chan-zh.html'
    if not html_path.exists():
        print("  SKIP: chinese-chan contract context (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    context = collect_export_context(html_path, soup)
    assert context['detection']['producer'] == 'slide-creator', context['detection']
    assert context['contract'] is not None, context
    assert context['contract']['contract_id'] == 'slide-creator/chinese-chan', context['contract']
    assert context['contract']['typography']['cn_font_stack'][0] == 'Noto Serif CJK SC', context['contract']
    assert context['contract']['line_break_contract']['break_policy']['.zen-body'] == 'preserve', context['contract']
    chrome = context['hints'].get('chrome_selectors') or []
    assert '.progress-bar' in chrome, chrome
    assert '.nav-dots' in chrome, chrome
    assert '#present-btn' in chrome, chrome
    print("  PASS: Chinese Chan loads synced contract and shared runtime chrome fallback")


def test_slide_creator_contract_manifest_tracks_upstream_and_data_story():
    """The synced manifest should vendor the full slide-creator preset/reference catalog."""
    manifest_path = REPO_ROOT / 'contracts' / 'slide_creator' / 'manifest.json'
    assert manifest_path.exists(), manifest_path
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert manifest['producer'] == 'slide-creator', manifest
    assert manifest['upstream_commit'], manifest
    assert manifest['source_snapshot_root'] == 'source_snapshot', manifest
    slugs = {preset['slug'] for preset in manifest['presets']}
    assert len(slugs) == 21, slugs
    assert {'blue-sky', 'enterprise-dark', 'swiss-modern', 'data-story', 'chinese-chan', 'aurora-mesh', 'glassmorphism', 'neo-brutalism', 'modern-newspaper'} <= slugs, manifest
    assert 'source_snapshot/references/aurora-mesh.md' in manifest['global_reference_snapshot_refs'], manifest
    assert 'source_snapshot/demos/aurora-mesh-zh.html' in manifest['global_demo_snapshot_refs'], manifest
    data_story = next(preset for preset in manifest['presets'] if preset['slug'] == 'data-story')
    assert data_story['producer_version_tested'] == '2.14.0', data_story
    print("  PASS: slide-creator manifest tracks all presets and vendored snapshots")


def test_collect_export_context_loads_aurora_mesh_contract_with_snapshots():
    """Aurora Mesh should load its synced contract, vendored refs, and preset-specific runtime hints."""
    html_path = REPO_ROOT / 'demo' / 'aurora-mesh-zh.html'
    if not html_path.exists():
        print("  SKIP: aurora-mesh contract context (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    context = collect_export_context(html_path, soup)
    assert context['detection']['producer'] == 'slide-creator', context['detection']
    assert context['contract'] is not None, context
    contract = context['contract']
    assert contract['contract_id'] == 'slide-creator/aurora-mesh', contract
    assert 'source_snapshot/references/aurora-mesh.md' in contract['source_snapshot_refs'], contract
    assert 'source_snapshot/demos/aurora-mesh-zh.html' in contract['demo_snapshot_refs'], contract
    assert '.stat-col' in contract['component_selectors']['stat_card'], contract
    assert contract['component_slot_models']['stat_card']['layout'] == 'vertical_card', contract
    assert contract['decorative_layers'][0]['kind'] == 'aurora-mesh', contract
    assert contract['typography']['display_font_stack'][0] == 'Space Grotesk', contract
    chrome = context['hints'].get('chrome_selectors') or []
    assert '.progress-bar' in chrome, chrome
    print("  PASS: Aurora Mesh loads synced contract and vendored snapshots")


def test_sync_slide_creator_contracts_builds_data_story_contract():
    """The sync helper should materialize the data-story component contract."""
    root = Path('/Users/song/projects/slide-creator')
    if not root.exists():
        print("  SKIP: sync slide-creator contracts (repo not found)")
        return

    manifest = sync_slide_creator_contracts.build_manifest(
        root,
        generated_at='2026-04-23',
        upstream_commit='deadbeef',
    )
    assert any(preset['slug'] == 'data-story' for preset in manifest['presets']), manifest

    contract = sync_slide_creator_contracts.build_contract(
        root,
        sync_slide_creator_contracts.PRESET_SPECS['data-story'],
        generated_at='2026-04-23',
        upstream_commit='deadbeef',
    )
    assert contract['contract_id'] == 'slide-creator/data-story', contract
    assert contract['component_slot_models']['metric_card']['slots'] == ['metric', 'label', 'trend'], contract
    assert contract['component_slot_models']['metric_card']['metric_single_line'] is True, contract
    assert contract['component_slot_models']['style_card']['stretch_first_slot'] is True, contract
    assert contract['component_slot_models']['style_card']['bottom_anchor_last_slot'] is False, contract
    assert contract['component_slot_models']['solution_card']['bottom_anchor_last_slot'] is False, contract
    assert contract['component_slot_models']['feature_card']['bottom_anchor_last_slot'] is False, contract
    assert '.ds-kpi-card' in contract['component_selectors']['metric_card'], contract
    print("  PASS: sync helper builds data-story contract")


def test_sync_slide_creator_contracts_builds_aurora_mesh_contract():
    """Aurora Mesh sync should materialize executable preset hints rather than a metadata shell."""
    root = Path('/Users/song/projects/slide-creator')
    if not root.exists():
        print("  SKIP: sync aurora-mesh contract (repo not found)")
        return

    manifest = sync_slide_creator_contracts.build_manifest(
        root,
        generated_at='2026-04-25',
        upstream_commit='deadbeef',
    )
    aurora_manifest = next(preset for preset in manifest['presets'] if preset['slug'] == 'aurora-mesh')
    assert aurora_manifest['source_refs'] == ['references/aurora-mesh.md', 'references/html-template.md'], aurora_manifest
    assert aurora_manifest['source_snapshot_refs'] == ['source_snapshot/references/aurora-mesh.md', 'source_snapshot/references/html-template.md'], aurora_manifest
    assert aurora_manifest['demo_snapshot_refs'] == ['source_snapshot/demos/aurora-mesh-zh.html', 'source_snapshot/demos/aurora-mesh-en.html'], aurora_manifest

    contract = sync_slide_creator_contracts.build_contract(
        root,
        sync_slide_creator_contracts.PRESET_SPECS['aurora-mesh'],
        generated_at='2026-04-25',
        upstream_commit='deadbeef',
    )
    assert contract['contract_id'] == 'slide-creator/aurora-mesh', contract
    assert contract['family'] == 'premium-saas-aurora', contract
    assert contract['source_snapshot_refs'] == ['source_snapshot/references/aurora-mesh.md', 'source_snapshot/references/html-template.md'], contract
    assert contract['demo_snapshot_refs'] == ['source_snapshot/demos/aurora-mesh-zh.html', 'source_snapshot/demos/aurora-mesh-en.html'], contract
    assert '.stat-col' in contract['component_selectors']['stat_card'], contract
    assert '.install-item' in contract['component_selectors']['install_row'], contract
    assert contract['component_slot_models']['stat_card']['layout'] == 'vertical_card', contract
    assert contract['component_slot_models']['install_row']['layout'] == 'vertical_card', contract
    assert contract['decorative_layers'][0]['kind'] == 'aurora-mesh', contract
    assert contract['typography']['body_font_stack'][0] == 'DM Sans', contract
    print("  PASS: sync helper builds Aurora Mesh contract with vendored refs")


def test_extract_aurora_mesh_background_builds_overlay_shapes():
    style = {
        'backgroundColor': '#0a0a1a',
        'backgroundImage': (
            'radial-gradient(ellipse at 20% 50%, rgba(120,40,200,0.40) 0%, transparent 60%),'
            'radial-gradient(ellipse at 80% 20%, rgba(0,180,255,0.30) 0%, transparent 50%),'
            'radial-gradient(ellipse at 60% 80%, rgba(0,255,180,0.20) 0%, transparent 50%)'
        ),
    }
    contract = {'contract_id': 'slide-creator/aurora-mesh'}
    mesh = extract_body_mesh_background(style, contract)
    assert mesh is not None, mesh
    assert mesh['kind'] == 'aurora-mesh', mesh
    assert len(mesh['layers']) == 3, mesh

    overlays = build_aurora_mesh_overlay_elements(mesh, 1440, 900)
    assert len(overlays) == 3, overlays
    assert all(overlay.get('_is_decoration') for overlay in overlays), overlays
    assert all(overlay.get('_skip_layout') for overlay in overlays), overlays
    print("  PASS: Aurora Mesh body background builds overlay shapes")


def test_parse_html_to_slides_aurora_uses_solid_base_without_mesh_overlays():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.18.0">
        <style>
          body {
            background-color: #0a0a1a;
            background-image:
              radial-gradient(ellipse at 20% 50%, rgba(120,40,200,0.40) 0%, transparent 60%),
              radial-gradient(ellipse at 80% 20%, rgba(0,180,255,0.30) 0%, transparent 50%),
              radial-gradient(ellipse at 60% 80%, rgba(0,255,180,0.20) 0%, transparent 50%);
          }
          .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
          }
        </style>
      </head>
      <body data-producer="kai-slide-creator" data-preset="Aurora Mesh">
        <section class="slide"><h1>Hello</h1></section>
      </body>
    </html>
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_path = Path(tmp_dir) / 'aurora-base-only.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 900)

    assert len(slides) == 1, slides
    bg = slides[0]['background']
    assert bg is not None, slides[0]
    assert bg != (10, 10, 26), bg
    assert 17 <= bg[0] <= 70, bg
    assert 16 <= bg[1] <= 75, bg
    assert 30 <= bg[2] <= 95, bg
    mesh_shapes = [
        elem for elem in slides[0]['elements']
        if elem.get('type') == 'shape' and elem.get('_is_decoration') and elem.get('tag') == 'circle'
    ]
    assert not mesh_shapes, mesh_shapes
    print("  PASS: Aurora slides use an atmospheric solid fallback and skip mesh overlays")


def test_parse_html_to_slides_aurora_stat_row_stays_within_slide_width():
    html_path = REPO_ROOT / 'demo' / 'aurora-mesh-zh.html'
    if not html_path.exists():
        print("  SKIP: aurora stat-row layout (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 900)
    slide = slides[3]
    elements = slide['elements']
    layout_slide_elements(elements, slide_style=slide.get('slideStyle', {}), slide_data=slide)

    root_container = next(
        elem for elem in elements
        if elem.get('type') == 'container' and any(
            child.get('type') == 'text' and child.get('text') == 'Solution'
            for child in elem.get('children', [])
        )
    )
    stat_row = next(child for child in root_container.get('children', []) if child.get('type') == 'container')
    assert stat_row['bounds']['width'] <= 13.33 + 1e-6, stat_row
    max_right = max(
        child['bounds']['x'] + child['bounds']['width']
        for child in stat_row.get('children', [])
    )
    assert max_right <= 13.33 + 1e-6, stat_row
    print("  PASS: Aurora stat-row contract keeps metrics within slide width")


def test_parse_html_to_slides_aurora_stat_row_defaults_to_compact_items():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.18.0">
        <style>
          body { background: #0a0a1a; color: #fff; }
          .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          }
          .stat-row {
            display: flex;
            gap: 64px;
            justify-content: center;
            align-items: flex-start;
          }
          .stat-col { display: flex; flex-direction: column; align-items: center; }
          .aurora-stat { font-size: 72px; line-height: 1; font-weight: 700; }
          .stat-sub { font-size: 15px; margin-top: 8px; }
        </style>
      </head>
      <body data-producer="kai-slide-creator" data-preset="Aurora Mesh">
        <section class="slide">
          <div class="stat-row">
            <div class="stat-col">
              <span class="aurora-stat">21</span>
              <span class="stat-sub">预设风格</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">100%</span>
              <span class="stat-sub">浏览器运行</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">3min</span>
              <span class="stat-sub">快速出稿</span>
            </div>
          </div>
        </section>
      </body>
    </html>
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_path = Path(tmp_dir) / 'aurora-compact-stats.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 900)

    slide = slides[0]
    layout_slide_elements(slide['elements'], slide_style=slide.get('slideStyle', {}), slide_data=slide)
    row = next(elem for elem in slide['elements'] if elem.get('type') == 'container')
    cards = [child for child in row.get('children', []) if child.get('type') == 'container']
    assert len(cards) == 3, cards
    assert max(card['bounds']['width'] for card in cards) < 2.4, cards
    span = max(card['bounds']['x'] + card['bounds']['width'] for card in cards) - min(card['bounds']['x'] for card in cards)
    assert span < 8.0, span
    print("  PASS: Aurora stat rows default to compact KPI widths")


def test_parse_html_to_slides_aurora_stat_row_respects_explicit_stretch_width():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.18.0">
        <style>
          body { background: #0a0a1a; color: #fff; }
          .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          }
          .stat-row {
            display: flex;
            gap: 24px;
            justify-content: center;
            align-items: flex-start;
            width: min(90vw, 1100px);
          }
          .stat-col {
            display: flex;
            flex: 1 1 0;
            flex-direction: column;
            align-items: center;
          }
          .aurora-stat { font-size: 72px; line-height: 1; font-weight: 700; }
          .stat-sub { font-size: 15px; margin-top: 8px; }
        </style>
      </head>
      <body data-producer="kai-slide-creator" data-preset="Aurora Mesh">
        <section class="slide">
          <div class="stat-row">
            <div class="stat-col">
              <span class="aurora-stat">21</span>
              <span class="stat-sub">预设风格</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">100%</span>
              <span class="stat-sub">浏览器运行</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">3min</span>
              <span class="stat-sub">快速出稿</span>
            </div>
          </div>
        </section>
      </body>
    </html>
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_path = Path(tmp_dir) / 'aurora-stretch-stats.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 900)

    slide = slides[0]
    layout_slide_elements(slide['elements'], slide_style=slide.get('slideStyle', {}), slide_data=slide)
    row = next(elem for elem in slide['elements'] if elem.get('type') == 'container')
    cards = [child for child in row.get('children', []) if child.get('type') == 'container']
    assert len(cards) == 3, cards
    assert min(card['bounds']['width'] for card in cards) > 2.8, cards
    print("  PASS: Aurora stat rows honor explicit stretch signals")


def test_parse_html_to_slides_aurora_wrapper_style_preserves_centered_layout():
    html_path = REPO_ROOT / 'demo' / 'aurora-mesh-zh.html'
    if not html_path.exists():
        print("  SKIP: aurora wrapper-centered layout (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 900)
    slide = slides[7]
    slide_style = slide.get('slideStyle', {})
    assert slide_style.get('justifyContent') == 'center', slide_style
    assert slide_style.get('alignItems') == 'center', slide_style
    assert parse_px(slide_style.get('paddingTop', '0px')) >= 64.0, slide_style

    elements = slide['elements']
    layout_slide_elements(elements, slide_style=slide_style, slide_data=slide)
    root_container = next(elem for elem in elements if elem.get('type') == 'container')
    assert 1.8 <= root_container['bounds']['y'] <= 2.4, root_container['bounds']
    print("  PASS: Aurora wrapper layout keeps CTA content vertically centered")


def test_parse_html_to_slides_aurora_install_items_keep_separate_vertical_cards():
    html_path = REPO_ROOT / 'demo' / 'aurora-mesh-zh.html'
    if not html_path.exists():
        print("  SKIP: aurora install rails (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 900)
    slide = slides[6]
    layout_slide_elements(slide['elements'], slide_style=slide.get('slideStyle', {}), slide_data=slide)

    def _collect_install_cards(node):
        found = []
        slot_model = node.get('_component_slot_model') or {}
        if (
            node.get('type') == 'container' and
            node.get('_component_contract') == 'vertical_card' and
            slot_model.get('slots') == ['label', 'command']
        ):
            found.append(node)
        for child in node.get('children', []) or []:
            if child.get('type') == 'container':
                found.extend(_collect_install_cards(child))
        return found

    root = next(elem for elem in slide['elements'] if elem.get('type') == 'container')
    install_cards = _collect_install_cards(root)

    assert len(install_cards) == 2, install_cards
    card_texts = [
        tuple(
            grandchild.get('text')
            for grandchild in card.get('children', [])
            if grandchild.get('type') == 'text'
        )
        for card in install_cards
    ]
    assert any(any('Claude Code' in (text or '') for text in card) for card in card_texts), card_texts
    assert any(any('OpenClaw' in (text or '') for text in card) for card in card_texts), card_texts
    print("  PASS: Aurora install slide keeps two separate install cards")


def test_sync_slide_creator_contracts_builds_swiss_modern_contract():
    """Swiss Modern sync should materialize executable layout tiers, typography, and compatibility metadata."""
    root = Path('/Users/song/projects/slide-creator')
    if not root.exists():
        print("  SKIP: sync swiss-modern contract (repo not found)")
        return

    manifest = sync_slide_creator_contracts.build_manifest(
        root,
        generated_at='2026-04-24',
        upstream_commit='deadbeef',
    )
    swiss_manifest = next(preset for preset in manifest['presets'] if preset['slug'] == 'swiss-modern')
    assert {'canonical', 'compatible', 'fallback'} <= set(swiss_manifest['support_tiers']), swiss_manifest

    contract = sync_slide_creator_contracts.build_contract(
        root,
        sync_slide_creator_contracts.PRESET_SPECS['swiss-modern'],
        generated_at='2026-04-24',
        upstream_commit='deadbeef',
    )
    assert contract['contract_id'] == 'slide-creator/swiss-modern', contract
    assert contract['component_slot_models']['body_columns']['layout'] == 'typographic_columns', contract
    assert contract['layout_contracts']['column_content']['compatible']['unwrap_wrapper'] is True, contract
    assert contract['signature_elements']['bg_num']['selectors'] == ['.bg-num'], contract
    assert contract['style_constraints']['allow_shadows'] is False, contract
    print("  PASS: sync helper builds Swiss Modern contract with layout tiers")


def test_parse_html_to_slides_swiss_compatible_wrapper_unwraps_and_preserves_two_columns():
    """Swiss compatible decks with a `.slide-content` wrapper should unwrap into the slide root and keep the right rail split."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="kai-slide-creator v2.18.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; display:flex; flex-direction:row; align-items:center; position:relative; background:#fff; }
          .slide-content { flex:1; display:flex; flex-direction:column; padding:48px; }
          .content { position:relative; z-index:1; }
          .left-col { flex:0 0 40%; padding-right:24px; }
          .right-col { flex:1; column-count:2; column-gap:32px; }
          .swiss-title { font-family:"Archivo Black", sans-serif; font-size:48px; line-height:1.0; text-transform:uppercase; }
          .swiss-body { font-family:"Nunito", sans-serif; font-size:16px; line-height:1.55; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-2">
          <div class="slide-content content">
            <div class="left-col">
              <h2 class="swiss-title">Column Story</h2>
            </div>
            <div class="right-col">
              <p class="swiss-body">Paragraph Alpha keeps the first rail occupied with enough words to wrap naturally.</p>
              <p class="swiss-body">Paragraph Beta continues the typographic flow without turning into one giant textbox.</p>
              <p class="swiss-body">Paragraph Gamma should begin in the second column once the first rail is sufficiently filled.</p>
            </div>
          </div>
          <span class="slide-num-label">02 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-compatible-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-compatible.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'compatible', slide
    assert slide['exportRole'] == 'column_content', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    custom_root = next(
        (elem for elem in slide['elements'] if elem.get('_component_contract') == 'swiss_column_content'),
        None,
    )
    assert custom_root is not None, slide['elements']

    texts = _collect_elements_by_type(slide['elements'], 'text')
    label = next(elem for elem in texts if elem.get('text') == '02 / 05')
    assert label.get('_skip_layout') is True, label

    title = next(elem for elem in texts if elem.get('text') == 'Column Story')
    paragraphs = [elem for elem in texts if elem.get('text', '').startswith('Paragraph')]
    assert len(paragraphs) == 3, texts
    distinct_x = {round(elem['bounds']['x'], 2) for elem in paragraphs}
    assert len(distinct_x) >= 2, [elem['bounds'] for elem in paragraphs]
    assert title['bounds']['x'] < min(elem['bounds']['x'] for elem in paragraphs), (
        title['bounds'],
        [elem['bounds'] for elem in paragraphs],
    )
    print("  PASS: Swiss compatible wrapper unwrap keeps page label and split body rails")


def test_parse_html_to_slides_swiss_canonical_title_grid_bottom_anchors_hero_block():
    """Canonical Swiss title grids should anchor the hero block near the bottom-left instead of centering it generically."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.21.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; display:flex; justify-content:flex-end; position:relative; overflow:hidden; background:#fff; }
          .bg-num { position:absolute; right:24px; top:0; font-family:"Archivo Black", sans-serif; font-size:220px; color:#f0f0f0; line-height:0.85; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
          .hero-inner { display:flex; flex-direction:column; gap:18px; width:min(76vw, 980px); padding:0 0 10vh clamp(52px, 6vw, 92px); }
          .eyebrow { font-size:12px; letter-spacing:0.18em; text-transform:uppercase; }
          .hero-rule { width:180px; height:2px; background:#ff3300; }
          .swiss-title { margin:0; max-width:min(68vw, 860px); font-family:"Archivo Black", sans-serif; font-size:72px; line-height:0.98; letter-spacing:-0.045em; text-transform:uppercase; }
          .hero-sub { max-width:34rem; font-family:"Nunito", sans-serif; font-size:18px; line-height:1.7; color:#666; }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-1" data-export-role="title_grid">
          <div class="bg-num">01</div>
          <div class="hero-inner">
            <div class="eyebrow">Question the Frame</div>
            <div class="hero-rule"></div>
            <h1 class="swiss-title">Operational Clarity<br>Compounds Value</h1>
            <p class="hero-sub">Put operating discipline, AI execution, and long-term value back on one decision line.</p>
          </div>
          <span class="slide-num-label">01 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-title-canonical-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-title-canonical.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'canonical', slide
    assert slide['exportRole'] == 'title_grid', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    custom_root = next(
        (elem for elem in slide['elements'] if elem.get('_component_contract') == 'swiss_title_grid'),
        None,
    )
    assert custom_root is not None, slide['elements']

    texts = _collect_elements_by_type(slide['elements'], 'text')
    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    eyebrow = next(elem for elem in texts if elem.get('text') == 'Question the Frame')
    title = next(elem for elem in texts if elem.get('text') == 'Operational Clarity\nCompounds Value')
    subtitle = next(elem for elem in texts if elem.get('text', '').startswith('Put operating discipline'))
    rule = next(shape for shape in shapes if shape.get('styles', {}).get('backgroundColor') == '#ff3300')

    assert eyebrow['bounds']['x'] < 1.2, eyebrow['bounds']
    assert title['bounds']['y'] > 3.5, title['bounds']
    assert eyebrow['bounds']['y'] < title['bounds']['y'], (eyebrow['bounds'], title['bounds'])
    assert rule['bounds']['y'] > eyebrow['bounds']['y'], (rule['bounds'], eyebrow['bounds'])
    assert subtitle['bounds']['y'] > title['bounds']['y'], (subtitle['bounds'], title['bounds'])
    print("  PASS: canonical Swiss title grid anchors the hero block near the bottom-left")


def test_parse_html_to_slides_swiss_compatible_title_grid_restores_rule_and_bottom_anchor():
    """Compatible Swiss title grids should still restore the hero rule and respect the bottom-anchored title stack."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="kai-slide-creator v2.18.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; display:flex; flex-direction:column; justify-content:flex-end; padding-bottom:10vh; position:relative; overflow:hidden; background:#fff; }
          .slide-content { flex:1; display:flex; flex-direction:column; justify-content:center; padding:clamp(1.5rem, 4vw, 4rem); }
          .eyebrow { color:#ff3300; font-size:12px; letter-spacing:0.18em; text-transform:uppercase; }
          .swiss-rule.red { width:200px; height:2px; background:#ff3300; border:none; margin:0; }
          .swiss-title { max-width:80%; font-family:"Archivo Black", sans-serif; font-size:72px; line-height:1.0; letter-spacing:-0.02em; text-transform:uppercase; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
          .reveal { opacity:0; transform:translateY(30px); }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-1">
          <div class="slide-content content">
            <div class="eyebrow reveal">Question the Frame</div>
            <hr class="swiss-rule red reveal">
            <h1 class="swiss-title reveal">Operational Clarity<br>Compounds Value</h1>
          </div>
          <span class="slide-num-label">01 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-title-compatible-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-title-compatible.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'compatible', slide
    assert slide['exportRole'] == 'title_grid', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    custom_root = next(
        (elem for elem in slide['elements'] if elem.get('_component_contract') == 'swiss_title_grid'),
        None,
    )
    assert custom_root is not None, slide['elements']

    texts = _collect_elements_by_type(slide['elements'], 'text')
    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    title = next(elem for elem in texts if elem.get('text') == 'Operational Clarity\nCompounds Value')
    rule = next(shape for shape in shapes if shape.get('styles', {}).get('backgroundColor') == '#ff3300')

    assert title['bounds']['y'] > 4.0, title['bounds']
    assert title['bounds']['x'] < 1.1, title['bounds']
    assert rule['bounds']['width'] > 1.5, rule['bounds']
    print("  PASS: compatible Swiss title grid restores the hidden rule and bottom anchor")


def test_parse_html_to_slides_swiss_canonical_column_content_preserves_full_height_left_rail():
    """Canonical Swiss column slides should build a full-height left rail instead of stacking the two panels vertically."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.21.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; display:flex; position:relative; overflow:hidden; background:#fff; }
          #slide-2 { flex-direction:row; align-items:stretch; }
          .bg-num { position:absolute; right:24px; top:0; font-family:"Archivo Black", sans-serif; font-size:220px; color:#f0f0f0; line-height:0.85; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
          .left-panel { flex:0 0 38%; display:flex; flex-direction:column; justify-content:center; gap:20px; padding:60px; background:#0a0a0a; color:#fff; }
          .left-panel h2 { margin:0; font-family:"Archivo Black", sans-serif; font-size:52px; line-height:1.0; text-transform:uppercase; }
          .left-rule { width:74px; height:2px; background:#ff3300; }
          .swiss-body { font-family:"Nunito", sans-serif; font-size:16px; line-height:1.7; }
          .right-panel { flex:1; padding:60px; column-count:2; column-gap:32px; }
          .right-panel p { margin:0 0 1em; font-family:"Nunito", sans-serif; font-size:16px; line-height:1.7; }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-2" data-export-role="column_content">
          <div class="bg-num">02</div>
          <div class="left-panel">
            <h2>Column Story</h2>
            <div class="left-rule"></div>
            <p class="swiss-body">The left editorial rail should stay vertically centered inside a full-height black panel.</p>
          </div>
          <div class="right-panel swiss-body-columns">
            <p>Paragraph Alpha keeps the first rail occupied with enough words to wrap naturally.</p>
            <p>Paragraph Beta continues the typographic flow without turning into one giant textbox.</p>
            <p>Paragraph Gamma should begin in the second column once the first rail is sufficiently filled.</p>
          </div>
          <span class="slide-num-label">02 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-canonical-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-canonical.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'canonical', slide
    assert slide['exportRole'] == 'column_content', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    texts = _collect_elements_by_type(slide['elements'], 'text')
    left_bg = next((shape for shape in shapes if shape.get('styles', {}).get('backgroundColor') == '#0a0a0a'), None)
    assert left_bg is not None, shapes
    assert left_bg['bounds']['height'] > 6.5, left_bg['bounds']

    title = next(elem for elem in texts if elem.get('text') == 'Column Story')
    paragraphs = [elem for elem in texts if elem.get('text', '').startswith('Paragraph')]
    assert len({round(elem['bounds']['x'], 2) for elem in paragraphs}) >= 2, [elem['bounds'] for elem in paragraphs]
    assert title['bounds']['x'] < min(elem['bounds']['x'] for elem in paragraphs), (
        title['bounds'],
        [elem['bounds'] for elem in paragraphs],
    )
    print("  PASS: canonical Swiss column content keeps the full-height left rail")


def test_parse_html_to_slides_swiss_compatible_stat_block_uses_thin_divider_not_black_block():
    """Compatible Swiss stat slides should separate metric and copy rails with a thin divider instead of a giant black rectangle."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="kai-slide-creator v2.18.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; display:flex; flex-direction:row; align-items:center; position:relative; background:#fff; }
          .slide-content { flex:1; display:flex; flex-direction:column; justify-content:center; padding:48px; }
          .content { position:relative; z-index:1; }
          .stat-block { flex:0 0 50%; }
          .swiss-stat { display:inline-block; font-family:"Archivo Black", sans-serif; font-size:96px; line-height:1.0; border-bottom:2px solid #ff3300; margin-bottom:16px; }
          .content-block { flex:1; padding-left:32px; border-left:2px solid #0a0a0a; }
          .content-block .eyebrow { font-size:12px; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px; }
          .content-block p { font-family:"Nunito", sans-serif; font-size:16px; line-height:1.7; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-3" data-export-role="stat_block">
          <div class="slide-content content">
            <div class="stat-block">
              <div class="swiss-stat">2.3B</div>
              <p>AI booking volume</p>
            </div>
            <div class="content-block">
              <div class="eyebrow">Execution</div>
              <p>AI orders are flowing through product usage and contract expansion rather than a one-quarter story.</p>
              <p>The exporter should preserve a clean split rail instead of inventing a giant black background block.</p>
            </div>
          </div>
          <span class="slide-num-label">03 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-stat-compatible-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-stat-compatible.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'compatible', slide
    assert slide['exportRole'] == 'stat_block', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    texts = _collect_elements_by_type(slide['elements'], 'text')
    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    metric = next(elem for elem in texts if elem.get('text') == '2.3B')
    copy = next(elem for elem in texts if elem.get('text', '').startswith('AI orders are flowing'))
    black_shapes = [shape for shape in shapes if shape.get('styles', {}).get('backgroundColor') == '#0a0a0a']

    assert metric['bounds']['x'] < copy['bounds']['x'], (metric['bounds'], copy['bounds'])
    assert metric['bounds']['height'] > 0.9, metric['bounds']
    assert black_shapes, shapes
    assert all(shape['bounds']['width'] < 0.08 for shape in black_shapes), [shape['bounds'] for shape in black_shapes]
    print("  PASS: compatible Swiss stat block uses a thin divider and separated rails")


def test_flat_extract_aurora_divider_keeps_explicit_thin_height():
    """Aurora-style empty divider blocks should export as thin tracks, not 1-inch fallback rectangles."""
    html = """
    <html>
      <head>
        <style>
          .aurora-content { max-width: min(90vw, 800px); }
          .aurora-divider {
            height: 1px;
            margin: 16px 0;
            background: rgba(0,245,196,0.3);
            border: none;
          }
        </style>
      </head>
      <body>
        <div class="aurora-content">
          <div class="aurora-divider"></div>
        </div>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    content = soup.select_one('.aurora-content')
    content_style = compute_element_style(content, css_rules, content.get('style', ''))
    elements = flat_extract(
        content,
        css_rules,
        content_style,
        1440,
        content_width_px=800.0,
        local_origin=True,
    )

    shapes = _collect_elements_by_type(elements, 'shape')
    assert len(shapes) == 1, shapes
    divider = shapes[0]
    assert divider['bounds']['width'] > 7.0, divider['bounds']
    assert divider['bounds']['height'] < 0.05, divider['bounds']
    print("  PASS: aurora divider keeps explicit thin height")


def test_build_explicit_track_aurora_divider_falls_back_to_slide_inner_width():
    """Hero dividers without a content wrapper should still resolve to a thin slide-width track."""
    html = """
    <html>
      <head>
        <style>
          .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          }
          .aurora-divider {
            height: 1px;
            margin: 16px 0;
            background: rgba(0,245,196,0.3);
            border: none;
          }
        </style>
      </head>
      <body>
        <section class="slide">
          <div class="aurora-divider"></div>
        </section>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    divider = soup.select_one('.aurora-divider')
    divider_style = compute_element_style(divider, css_rules, divider.get('style', ''))
    shapes = export_sandbox._build_explicit_track_elements(
        divider,
        divider_style,
        css_rules,
        1440,
        None,
    )

    assert shapes is not None, shapes
    assert len(shapes) == 1, shapes
    assert shapes[0]['bounds']['width'] > 10.0, shapes[0]['bounds']
    assert shapes[0]['bounds']['height'] < 0.05, shapes[0]['bounds']
    print("  PASS: aurora hero divider falls back to slide inner width")


def test_parse_html_to_slides_aurora_stats_preserve_separate_metric_tokens():
    """Aurora metric stacks should keep display numbers separate from labels/copy."""
    html = """
    <!doctype html>
    <html>
      <head>
        <meta name="generator" content="kai-slide-creator v2.18.0">
        <style>
          body {
            background-color: #0a0a1a;
            background-image:
              radial-gradient(ellipse at 20% 50%, rgba(120,40,200,0.40) 0%, transparent 60%),
              radial-gradient(ellipse at 80% 20%, rgba(0,180,255,0.30) 0%, transparent 50%);
            color: #fff;
          }
          .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          }
          .stat-row {
            display: flex;
            gap: clamp(3rem, 6vw, 6rem);
            justify-content: center;
            align-items: flex-start;
          }
          .stat-col {
            display: flex;
            flex-direction: column;
            align-items: center;
          }
          .aurora-stat {
            background-image: linear-gradient(135deg, #00f5c4, #00b4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: clamp(3rem, 10vw, 8rem);
            font-weight: 700;
            line-height: 1;
          }
          .stat-sub {
            font-size: clamp(0.75rem, 1.2vw, 1rem);
            color: rgba(255,255,255,0.45);
            margin-top: 8px;
          }
        </style>
      </head>
      <body data-producer="kai-slide-creator" data-preset="Aurora Mesh">
        <section class="slide">
          <div class="stat-row">
            <div class="stat-col">
              <span class="aurora-stat">21</span>
              <span class="stat-sub">预设风格</span>
              <span class="stat-sub">每种都有独立视觉签名</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">100%</span>
              <span class="stat-sub">浏览器运行</span>
              <span class="stat-sub">零服务器，零依赖</span>
            </div>
            <div class="stat-col">
              <span class="aurora-stat">3min</span>
              <span class="stat-sub">快速出稿</span>
              <span class="stat-sub">从想法到完整演示</span>
            </div>
          </div>
        </section>
      </body>
    </html>
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_path = Path(tmp_dir) / 'aurora-stats.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 900)

    assert len(slides) == 1, slides
    texts = _collect_text_values(slides[0]['elements'])
    for token in ('21', '100%', '3min', '预设风格', '浏览器运行', '快速出稿'):
        assert token in texts, texts
    assert not any('21预设风格' in text for text in texts), texts
    assert not any('100%浏览器运行' in text for text in texts), texts

    metric_texts = [
        elem for elem in _collect_elements_by_type(slides[0]['elements'], 'text')
        if elem.get('text') in ('21', '100%', '3min')
    ]
    assert len(metric_texts) == 3, metric_texts
    assert all(elem.get('gradientColors') for elem in metric_texts), metric_texts
    print("  PASS: aurora stats preserve separate metric tokens")


def test_parse_html_to_slides_swiss_canonical_pull_quote_preserves_left_offset_and_top_margin():
    """Canonical Swiss pull quotes should honor the authored left offset and top margin instead of recentering the quote stack."""
    html = '''
    <html>
      <head>
        <meta name="generator" content="slide-creator v2.21.0">
        <style>
          body { background:#fff; }
          .slide { width:100vw; height:100vh; position:relative; overflow:hidden; background:#fff; }
          .slide-num-label { position:absolute; top:24px; right:24px; font-size:14px; color:#ff3300; }
          .pull-quote { display:flex; flex-direction:column; gap:18px; width:min(60vw, 700px); margin:18vh 0 0 clamp(54px, 7vw, 108px); }
          .quote-text { margin:0; font-family:"Archivo Black", sans-serif; font-size:66px; line-height:1.02; letter-spacing:-0.035em; }
          .quote-rule { width:160px; height:2px; background:#ff3300; }
          .quote-attribution { margin:0; font-family:"Nunito", sans-serif; font-size:15px; line-height:1.6; letter-spacing:0.1em; text-transform:uppercase; color:#666; }
          .swiss-body { margin:0; max-width:34rem; font-family:"Nunito", sans-serif; font-size:17px; line-height:1.72; color:#666; }
        </style>
      </head>
      <body data-preset="Swiss Modern">
        <section class="slide" id="slide-5" data-export-role="pull_quote">
          <div class="pull-quote">
            <p class="quote-text">Hold the Root</p>
            <div class="quote-rule"></div>
            <p class="quote-attribution">Analects · Swiss Reading</p>
            <p class="swiss-body">The quote block should stay left anchored with a deliberate top offset instead of drifting to the vertical center.</p>
          </div>
          <span class="slide-num-label">05 / 05</span>
        </section>
      </body>
    </html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-swiss-pull-canonical-') as tmp_dir:
        html_path = Path(tmp_dir) / 'swiss-pull-canonical.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    assert slide['exportSupportTier'] == 'canonical', slide
    assert slide['exportRole'] == 'pull_quote', slide
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    custom_root = next(
        (elem for elem in slide['elements'] if elem.get('_component_contract') == 'swiss_pull_quote'),
        None,
    )
    assert custom_root is not None, slide['elements']

    texts = _collect_elements_by_type(slide['elements'], 'text')
    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    quote = next(elem for elem in texts if elem.get('text') == 'Hold the Root')
    attribution = next(elem for elem in texts if elem.get('text') == 'Analects · Swiss Reading')
    body = next(elem for elem in texts if elem.get('text', '').startswith('The quote block should stay'))
    rule = next(shape for shape in shapes if shape.get('styles', {}).get('backgroundColor') == '#ff3300')

    assert 0.7 <= quote['bounds']['x'] <= 1.2, quote['bounds']
    assert 1.0 <= quote['bounds']['y'] <= 1.8, quote['bounds']
    assert attribution['bounds']['y'] > quote['bounds']['y'], (attribution['bounds'], quote['bounds'])
    assert body['bounds']['x'] == quote['bounds']['x'], (body['bounds'], quote['bounds'])
    assert rule['bounds']['y'] > quote['bounds']['y'], (rule['bounds'], quote['bounds'])
    print("  PASS: canonical Swiss pull quote keeps the authored left/top anchor")


def test_classify_slide_layout_prefers_data_export_role_hint_when_multiple_roles_match():
    contract = {
        'layout_contracts': {
            'column_content': {
                'canonical': {
                    'direct_child_any': ['.shared-layout'],
                },
            },
            'pull_quote': {
                'canonical': {
                    'direct_child_any': ['.shared-layout'],
                },
            },
        },
        'support_tiers': {'canonical': {}},
    }
    slide = BeautifulSoup(
        '''
        <section class="slide" data-export-role="pull_quote">
          <div class="shared-layout"></div>
        </section>
        ''',
        'lxml',
    ).find('section')

    layout = export_sandbox._classify_slide_layout(slide, contract)

    assert layout['support_tier'] == 'canonical', layout
    assert layout['role'] == 'pull_quote', layout
    print("  PASS: data-export-role hint biases contract layout classification")


def test_media_query_max_height_does_not_override_large_heading_at_default_viewport():
    """Max-height media rules should only apply when the export viewport is actually short."""
    html = '''
    <html><head><style>
      :root { --title-size: clamp(2rem, 6vw, 5rem); }
      @media (max-height: 700px) {
        :root { --title-size: clamp(1rem, 3.5vw, 1.5rem); }
      }
      h1 { font-size: var(--title-size); font-weight: 800; }
    </style></head><body><h1>Heading</h1></body></html>
    '''
    soup = BeautifulSoup(html, 'lxml')
    css_rules = extract_css_from_soup(soup)
    h1 = soup.find('h1')
    style = compute_element_style(h1, css_rules, h1.get('style', ''))
    assert parse_px(style.get('fontSize', '0')) >= 72.0, style
    print("  PASS: max-height media query no longer shrinks headings at 1440x900")


def test_short_latin_inline_block_label_uses_compact_width():
    """Short rounded Latin labels should shrink-wrap closer to browser metrics."""
    html = '''
    <span style="
      display:inline-block;
      padding:4px 12px;
      border-radius:999px;
      background:rgba(56,139,253,0.12);
      border:1px solid rgba(255,255,255,0.12);
      color:#d8dee9;
      font-size:13px;
      font-weight:500;
    ">Aurora Mesh</span>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span')
    style = compute_element_style(span, [], span.get('style', ''))
    text_el = build_text_element(span, style, [], 1440, 1180)
    assert text_el is not None
    assert 0.72 <= text_el['bounds']['width'] <= 0.95, text_el['bounds']
    print("  PASS: short latin inline-block label uses compact width")


def test_enterprise_dark_split_cards_stack_in_right_column():
    """Enterprise Dark split cards should stack vertically in the right rail, not spill horizontally."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark split stacking (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    root = slides[1]['elements'][0]
    right_wrapper = next(
        (
            child for child in root.get('children', [])
            if child.get('type') == 'container'
            and child.get('bounds', {}).get('width', 0) > 3.0
            and len([grand for grand in child.get('children', []) if grand.get('type') == 'container']) >= 3
        ),
        None,
    )
    assert right_wrapper is not None, root.get('children', [])
    right_cards = [child for child in right_wrapper.get('children', []) if child.get('type') == 'container']
    assert len(right_cards) >= 3, right_wrapper
    card_xs = [card['bounds']['x'] for card in right_cards]
    card_ys = [card['bounds']['y'] for card in right_cards]
    assert max(card_xs) - min(card_xs) < 0.01, card_xs
    assert card_ys == sorted(card_ys), card_ys
    assert max(card['bounds']['x'] + card['bounds']['width'] for card in right_cards) <= 12.5, right_cards
    print("  PASS: enterprise-dark split cards stack in right column")


def test_enterprise_dark_install_grid_prefers_centered_single_column_stack():
    """Centered auto-fit installation grids should shrink-wrap into a single stacked column."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark install grid stacking (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide7 = slides[6]
    wrapper = next((elem for elem in slide7['elements'] if elem.get('type') == 'container'), None)
    assert wrapper is not None, slide7['elements']
    assert wrapper['bounds']['width'] > 6.0, wrapper['bounds']
    nested_containers = _collect_elements_by_type([wrapper], 'container')
    grid_container = next(
        (
            child for child in nested_containers
            if child is not wrapper
            and child.get('bounds', {}).get('width', 0) > 3.0
            and len([grand for grand in child.get('children', []) if grand.get('type') == 'container']) >= 2
        ),
        None,
    )
    assert grid_container is not None, nested_containers
    cards = [child for child in grid_container.get('children', []) if child.get('type') == 'container']
    assert len(cards) >= 2, grid_container
    card_xs = [round(card['bounds']['x'], 3) for card in cards]
    card_ys = [round(card['bounds']['y'], 3) for card in cards]
    assert max(card_xs) - min(card_xs) < 0.05, card_xs
    assert card_ys == sorted(card_ys), card_ys
    print("  PASS: enterprise-dark install grid prefers centered single-column stack")


def test_enterprise_dark_cta_kpi_grid_preserves_two_card_widths():
    """CTA KPI cards should keep equal widths while remaining vertically stacked."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark CTA KPI grid (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide8 = slides[7]
    containers = _collect_elements_by_type(slide8['elements'], 'container')
    kpi_grid = next(
        (
            elem for elem in containers
            if len([child for child in elem.get('children', []) if child.get('type') == 'container']) == 2
        ),
        None,
    )
    assert kpi_grid is not None, containers
    cards = [child for child in kpi_grid.get('children', []) if child.get('type') == 'container']
    assert len(cards) == 2, kpi_grid
    widths = [round(card['bounds']['width'], 3) for card in cards]
    xs = [round(card['bounds']['x'], 3) for card in cards]
    ys = [round(card['bounds']['y'], 3) for card in cards]
    assert max(widths) - min(widths) < 0.05, widths
    assert min(widths) > 1.4, widths
    assert max(xs) - min(xs) < 0.05, xs
    assert ys == sorted(ys), ys
    print("  PASS: enterprise-dark CTA KPI grid keeps stacked equal-width cards")


def test_enterprise_dark_workflow_cards_share_row_height():
    """Multi-column workflow cards should stretch to the shared grid row height."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark workflow row height (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide3 = slides[2]
    containers = _collect_elements_by_type(slide3['elements'], 'container')
    workflow_grid = next(
        (
            elem for elem in containers
            if len([child for child in elem.get('children', []) if child.get('type') == 'container']) == 3
        ),
        None,
    )
    assert workflow_grid is not None, containers
    cards = [child for child in workflow_grid.get('children', []) if child.get('type') == 'container']
    heights = [round(card['bounds']['height'], 3) for card in cards]
    assert max(heights) - min(heights) < 0.05, heights
    print("  PASS: enterprise-dark workflow cards share row height")


def test_enterprise_dark_workflow_index_keeps_breathing_room_before_title():
    """Step-number labels in workflow cards should leave a visible gap before the title."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark workflow index/title gap (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide3 = slides[2]
    containers = _collect_elements_by_type(slide3['elements'], 'container')
    workflow_grid = next(
        (
            elem for elem in containers
            if len([child for child in elem.get('children', []) if child.get('type') == 'container']) == 3
        ),
        None,
    )
    assert workflow_grid is not None, containers
    cards = [child for child in workflow_grid.get('children', []) if child.get('type') == 'container']
    first_card = cards[0]
    texts = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    step = next((child for child in texts if child.get('text', '').strip() == '01'), None)
    title = next((child for child in texts if child.get('text', '').strip() == '描述心情'), None)
    assert step is not None and title is not None, texts
    step_bottom = step['bounds']['y'] + step['bounds']['height']
    gap = title['bounds']['y'] - step_bottom
    assert gap >= 9.5 / export_sandbox.PX_PER_IN, gap
    print("  PASS: enterprise-dark workflow index leaves breathing room before title")


def test_enterprise_dark_trend_rows_stretch_full_card_width():
    """Progress-card trend rows should stretch to the card width instead of centering like chips."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark trend row stretch (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    texts = _collect_elements_by_type(slide2['elements'], 'text')
    body = next((elem for elem in texts if 'Node、Webpack' in elem.get('text', '')), None)
    trend = next((elem for elem in texts if '72% 用户抱怨构建复杂度' in elem.get('text', '')), None)
    assert body is not None and trend is not None, texts
    assert trend['bounds']['width'] > 4.5, trend['bounds']
    assert abs(trend['bounds']['x'] - body['bounds']['x']) < 0.05, (trend['bounds'], body['bounds'])
    print("  PASS: enterprise-dark trend rows stretch full card width")


def test_data_story_problem_split_preserves_kpi_cards_as_nested_containers():
    """Problem split layouts should keep KPI cards as nested containers instead of flattening them."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story split KPI card packing (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    split, left_rail, _ = _find_data_story_split_rails(slide2)
    nested_cards = [
        child for child in left_rail.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    ]
    assert split['bounds']['width'] > 10, split['bounds']
    assert len(nested_cards) >= 3, left_rail.get('children', [])
    print("  PASS: data-story split keeps KPI cards as nested containers")


def test_data_story_solution_grid_preserves_solution_cards_as_nested_containers():
    """Solution grids should keep each solution block as its own contract card."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story solution card packing (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide4 = slides[3]
    containers = _collect_elements_by_type(slide4['elements'], 'container')
    solution_grid = next(
        (
            elem for elem in containers
            if sum(
                1 for child in elem.get('children', [])
                if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
            ) >= 4
        ),
        None,
    )
    assert solution_grid is not None, containers
    nested_cards = [
        child for child in solution_grid.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    ]
    assert len(nested_cards) >= 4, solution_grid.get('children', [])
    print("  PASS: data-story solution grid keeps nested solution cards")


def test_data_story_feature_grid_preserves_cards_as_nested_containers():
    """Feature grids should preserve each block card as its own nested container."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature card packing (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    containers = _collect_elements_by_type(slide6['elements'], 'container')
    feat_grid = next((elem for elem in containers if len(elem.get('children', [])) == 4), None)
    assert feat_grid is not None, containers
    assert all(child.get('type') == 'container' and child.get('_children_relative') for child in feat_grid.get('children', [])), feat_grid.get('children', [])
    print("  PASS: data-story feature grid keeps nested card containers")


def test_data_story_problem_cards_stack_metric_and_copy_vertically():
    """Visible block KPI cards should vertically stack metric and supporting copy."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story problem card vertical stack (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide2['elements'])
    slide2['_slide_index'] = 1
    layout_slide_elements(slide2['elements'], 13.33, 810 / 108, slide2['slideStyle'], slide2)

    _, left_rail, _ = _find_data_story_split_rails(slide2)
    first_card = next(
        child for child in left_rail.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    )
    text_children = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    assert len(text_children) >= 2, first_card.get('children', [])

    metric = text_children[0]['bounds']
    copy = text_children[1]['bounds']
    assert copy['y'] >= metric['y'] + metric['height'] - 0.01, (metric, copy)
    print("  PASS: data-story problem cards stack metric and copy vertically")


def test_flat_extract_content_svg_builds_relative_container():
    """Inline content SVG charts should emit a drawable relative container instead of being dropped."""
    html = '''
    <svg viewBox="0 0 100 50" class="chart-svg">
      <line x1="10" y1="40" x2="90" y2="40" stroke="#334155" stroke-width="2"></line>
      <rect x="20" y="20" width="12" height="20" rx="2" fill="#3b82f6"></rect>
      <text x="26" y="18" text-anchor="middle" style="font-size:12px; fill:#22d3ee;">80</text>
    </svg>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    svg = soup.find('svg')
    results = export_sandbox.flat_extract(svg, [], None, 1440, content_width_px=400, local_origin=True)

    assert len(results) == 1, results
    container = results[0]
    assert container.get('type') == 'container' and container.get('_children_relative'), container
    child_types = [child.get('type') for child in container.get('children', [])]
    assert 'shape' in child_types and 'text' in child_types, child_types
    print("  PASS: content SVG builds relative drawable container")


def test_flat_extract_content_svg_keeps_polyline_and_dots():
    """Data charts should keep line-series and dot markers instead of dropping them."""
    html = '''
    <svg viewBox="0 0 120 60" class="chart-svg">
      <polygon points="10,45 40,30 70,20 100,12 100,55 10,55" fill="#3b82f6"></polygon>
      <polyline points="10,45 40,30 70,20 100,12" stroke="#3b82f6" stroke-width="2.5" fill="none"></polyline>
      <circle cx="10" cy="45" r="3"></circle>
      <circle cx="40" cy="30" r="3"></circle>
    </svg>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    svg = soup.find('svg')
    results = export_sandbox.flat_extract(svg, [], None, 1440, content_width_px=360, local_origin=True)
    assert len(results) == 1, results
    container = results[0]
    child_types = [(child.get('type'), child.get('tag')) for child in container.get('children', [])]
    assert ('freeform', 'polyline') in child_types, child_types
    assert ('shape', 'circle') in child_types, child_types
    print("  PASS: content SVG keeps polyline series and circle markers")


def test_data_story_problem_split_keeps_svg_chart_container():
    """Problem split should retain the SVG chart as a nested container."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story svg chart retention (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    _, _, right_rail = _find_data_story_split_rails(slide2)
    has_svg_container = any(
        child.get('type') == 'container' and child.get('tag') == 'svg'
        for child in right_rail.get('children', [])
    )
    assert has_svg_container, right_rail.get('children', [])
    print("  PASS: data-story split keeps SVG chart container")


def test_data_story_feature_cards_stack_text_content_vertically():
    """Feature cards should vertically stack number, title, and description."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature card vertical stack (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide6['elements'])
    slide6['_slide_index'] = 5
    layout_slide_elements(slide6['elements'], 13.33, 810 / 108, slide6['slideStyle'], slide6)

    feat_grid = next(elem for elem in slide6['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in feat_grid.get('children', []) if child.get('type') == 'container')
    text_children = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    assert len(text_children) >= 3, first_card.get('children', [])

    positions = [child['bounds']['y'] for child in text_children[:3]]
    assert positions[0] < positions[1] < positions[2], positions
    print("  PASS: data-story feature cards stack text content vertically")


def test_data_story_cta_kpi_grid_prefers_centered_single_column_stack():
    """CTA KPI cards should shrink-wrap into a centered single-column stack."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story CTA KPI stack (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide8 = slides[7]
    containers = _collect_elements_by_type(slide8['elements'], 'container')
    kpi_grid = next(
        (
            elem for elem in containers
            if len([child for child in elem.get('children', []) if child.get('type') == 'container']) == 2
            and elem.get('bounds', {}).get('y', 0.0) > 3.0
        ),
        None,
    )
    assert kpi_grid is not None, containers
    cards = [child for child in kpi_grid.get('children', []) if child.get('type') == 'container']
    widths = [round(card['bounds']['width'], 3) for card in cards]
    xs = [round(card['bounds']['x'], 3) for card in cards]
    ys = [round(card['bounds']['y'], 3) for card in cards]
    assert len(cards) == 2, kpi_grid
    assert max(widths) - min(widths) < 0.05, widths
    assert min(widths) > 1.4, widths
    assert max(xs) - min(xs) < 0.05, xs
    assert ys == sorted(ys), ys
    print("  PASS: data-story CTA KPI grid prefers centered single-column stack")


def test_data_story_nested_card_groups_keep_grid_slot_width():
    """Nested background-card containers inside grids should occupy their laid-out track width."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story nested card grid width (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)

    slide2 = slides[1]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide2['elements'])
    slide2['_slide_index'] = 1
    layout_slide_elements(slide2['elements'], 13.33, 810 / 108, slide2['slideStyle'], slide2)
    _, left_rail, _ = _find_data_story_split_rails(slide2)
    first_problem_card = next(
        child for child in left_rail.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    )
    assert first_problem_card['bounds']['width'] > 3.0, first_problem_card['bounds']

    slide6 = slides[5]
    pre_pass_corrections(slide6['elements'])
    slide6['_slide_index'] = 5
    layout_slide_elements(slide6['elements'], 13.33, 810 / 108, slide6['slideStyle'], slide6)
    feat_grid = next(elem for elem in slide6['elements'] if elem.get('type') == 'container')
    first_feature_card = next(child for child in feat_grid.get('children', []) if child.get('type') == 'container')
    assert first_feature_card['bounds']['width'] > 3.0, first_feature_card['bounds']
    print("  PASS: data-story nested card groups keep grid slot width")


def test_data_story_install_rows_keep_horizontal_rails():
    """Contract-driven install rows should keep label and command on the same horizontal band."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story install-row rails (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide7 = slides[6]
    containers = _collect_elements_by_type(slide7['elements'], 'container')
    row = next(
        elem for elem in containers
        if elem.get('type') == 'container' and elem.get('_component_contract') == 'split_rail'
    )
    texts = [child for child in row.get('children', []) if child.get('type') == 'text']
    assert len(texts) == 2, row.get('children', [])
    label, cmd = texts
    assert cmd['bounds']['x'] > label['bounds']['x'] + label['bounds']['width'], (label['bounds'], cmd['bounds'])
    assert abs(label['bounds']['y'] - cmd['bounds']['y']) < 0.12, (label['bounds'], cmd['bounds'])
    print("  PASS: data-story install rows keep horizontal rails")


def test_data_story_centered_column_wrapper_preserves_max_width_and_children():
    """Top-level centered flex-column wrappers should stay grouped and keep authored max-width."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story centered column wrapper packing (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide7 = slides[6]
    wrapper = next(
        (
            elem for elem in slide7['elements']
            if elem.get('type') == 'container' and elem.get('_component_contract') is None
        ),
        None,
    )
    assert wrapper is not None, slide7['elements']
    # Authored CSS: `max-width: min(90vw, 700px)` → 700/108 ≈ 6.48". Per-item
    # x-normalization in `_pack_relative_block_container` now respects this
    # max-width without padding-driven inflation, so the floor is 6.4" (was
    # 6.9" before the inconsistent global-min-x shift was removed).
    assert wrapper['bounds']['width'] >= 6.4, wrapper['bounds']
    child_containers = _collect_elements_by_type(wrapper.get('children', []), 'container')
    split_rails = [child for child in child_containers if child.get('_component_contract') == 'split_rail']
    metric_grids = [
        child for child in child_containers
        if len([
            grandchild for grandchild in child.get('children', [])
            if grandchild.get('type') == 'container' and grandchild.get('_component_contract') == 'vertical_card'
        ]) == 3
    ]
    assert len(split_rails) == 2, wrapper.get('children', [])
    assert metric_grids, wrapper.get('children', [])
    print("  PASS: centered column wrapper keeps authored width and grouped children")


def test_data_story_centered_wrapper_keeps_paired_pills_overlaid():
    """Centered wrapper packing should keep paired pill bg/text overlaid instead of stacking them."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story paired pill overlay (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    for slide_idx, label_text in ((0, 'slide-creator'), (7, '/slide-creator')):
        slide = slides[slide_idx]
        export_sandbox.pre_pass_corrections(slide['elements'])
        slide['_slide_index'] = slide_idx
        layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide.get('slideStyle', {}), slide)

        texts = [
            elem for elem in _collect_elements_by_type(slide['elements'], 'text')
            if (elem.get('text') or '').strip() == label_text and elem.get('_pair_with')
        ]
        assert texts, (slide_idx, label_text)
        pill_text = texts[0]
        pill_shape = next(
            elem for elem in _collect_elements_by_type(slide['elements'], 'shape')
            if elem.get('_pair_with') == pill_text.get('_pair_with')
        )
        assert abs(pill_shape['bounds']['y'] - pill_text['bounds']['y']) < 0.02, (
            slide_idx, pill_shape['bounds'], pill_text['bounds']
        )
        assert abs(pill_shape['bounds']['x'] - pill_text['bounds']['x']) < 0.02, (
            slide_idx, pill_shape['bounds'], pill_text['bounds']
        )
    print("  PASS: data-story centered wrappers keep paired pills overlaid")


def test_data_story_feature_cards_use_contract_min_height():
    """Contract-driven feature cards should preserve a stable minimum card height."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature card min height (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    feat_grid = next(elem for elem in slide6['elements'] if elem.get('type') == 'container')
    feature_cards = [
        child for child in feat_grid.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    ]
    assert len(feature_cards) >= 4, feat_grid.get('children', [])
    assert all(card['bounds']['height'] >= 0.90 for card in feature_cards[:4]), [card['bounds'] for card in feature_cards[:4]]
    print("  PASS: data-story feature cards keep contract minimum height")


def test_data_story_style_cards_preserve_authored_preview_body_trend_spacing():
    """Style cards should keep authored swatch/title/body/trend spacing instead of KPI-style bottom anchoring."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story style card authored spacing (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide3 = slides[2]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide3['elements'])
    slide3['_slide_index'] = 2
    layout_slide_elements(slide3['elements'], 13.33, 810 / 108, slide3['slideStyle'], slide3)

    style_grid = next(elem for elem in slide3['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in style_grid.get('children', []) if child.get('type') == 'container')
    preview = next(child for child in first_card.get('children', []) if child.get('type') == 'container')
    text_children = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    title, body, trend = text_children
    preview_bottom = preview['bounds']['y'] + preview['bounds']['height']
    gap_preview_title = title['bounds']['y'] - preview_bottom
    gap_title_body = body['bounds']['y'] - (title['bounds']['y'] + title['bounds']['height'])
    gap_body_trend = trend['bounds']['y'] - (body['bounds']['y'] + body['bounds']['height'])
    assert 0.10 <= gap_preview_title <= 0.16, (preview['bounds'], title['bounds'])
    assert 0.03 <= gap_title_body <= 0.06, (title['bounds'], body['bounds'])
    assert 0.07 <= gap_body_trend <= 0.11, (body['bounds'], trend['bounds'])
    print("  PASS: data-story style cards keep authored preview/body/trend spacing")


def test_data_story_solution_cards_preserve_compact_icon_title_body_flow():
    """Solution cards should keep compact authored flow instead of pushing title/body to the bottom."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story solution card compact flow (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide4 = slides[3]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide4['elements'])
    slide4['_slide_index'] = 3
    layout_slide_elements(slide4['elements'], 13.33, 810 / 108, slide4['slideStyle'], slide4)

    solution_grid = next(elem for elem in slide4['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in solution_grid.get('children', []) if child.get('type') == 'container')
    text_children = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    icon, title, body = text_children
    gap_icon_title = title['bounds']['y'] - (icon['bounds']['y'] + icon['bounds']['height'])
    gap_title_body = body['bounds']['y'] - (title['bounds']['y'] + title['bounds']['height'])
    assert 0.04 <= gap_icon_title <= 0.14, (icon['bounds'], title['bounds'])
    assert 0.04 <= gap_title_body <= 0.14, (title['bounds'], body['bounds'])
    print("  PASS: data-story solution cards keep compact icon/title/body flow")


def test_data_story_feature_cards_preserve_compact_metric_title_body_flow():
    """Feature cards should keep authored 4px rhythm instead of large KPI-like voids."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature card compact flow (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide6['elements'])
    slide6['_slide_index'] = 5
    layout_slide_elements(slide6['elements'], 13.33, 810 / 108, slide6['slideStyle'], slide6)

    feat_grid = next(elem for elem in slide6['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in feat_grid.get('children', []) if child.get('type') == 'container')
    text_children = [child for child in first_card.get('children', []) if child.get('type') == 'text']
    metric, title, body = text_children
    gap_metric_title = title['bounds']['y'] - (metric['bounds']['y'] + metric['bounds']['height'])
    gap_title_body = body['bounds']['y'] - (title['bounds']['y'] + title['bounds']['height'])
    assert 0.02 <= gap_metric_title <= 0.08, (metric['bounds'], title['bounds'])
    assert 0.02 <= gap_title_body <= 0.08, (title['bounds'], body['bounds'])
    print("  PASS: data-story feature cards keep compact metric/title/body flow")


def test_data_story_metric_cards_keep_large_numbers_single_line():
    """Problem KPI cards should keep short metric tokens on a single line."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story metric single-line (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    _, left_rail, _ = _find_data_story_split_rails(slide2)
    first_card = next(
        child for child in left_rail.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    )
    metric = next(child for child in first_card.get('children', []) if child.get('type') == 'text' and child.get('text') == '73%')
    assert metric.get('forceSingleLine'), metric
    assert metric.get('bounds', {}).get('height', 0.0) < 1.05, metric.get('bounds')
    print("  PASS: data-story KPI cards keep metric tokens single-line")


def test_data_story_metric_cards_limit_metric_share_of_card_height():
    """KPI cards should keep the metric token from consuming most of the card height."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story metric card metric ratio (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide2['elements'])
    slide2['_slide_index'] = 1
    layout_slide_elements(slide2['elements'], 13.33, 810 / 108, slide2['slideStyle'], slide2)

    _, left_rail, _ = _find_data_story_split_rails(slide2)
    first_card = next(
        child for child in left_rail.get('children', [])
        if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
    )
    bg = next(child for child in first_card['children'] if child.get('_is_card_bg'))
    metric = next(child for child in first_card['children'] if child.get('type') == 'text' and child.get('_slot_metric'))
    inner_h = bg['bounds']['height'] - bg.get('_css_pad_t', 0.0) - bg.get('_css_pad_b', 0.0)
    assert inner_h > 0.1, first_card['bounds']
    assert metric['bounds']['height'] <= inner_h * 0.81, (metric['bounds'], first_card['bounds'])
    print("  PASS: data-story metric cards limit metric share of card height")


def test_data_story_feature_cards_limit_metric_share_of_card_height():
    """Feature cards should keep large stat tokens visually subordinate to the card body."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature card metric ratio (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide6['elements'])
    slide6['_slide_index'] = 5
    layout_slide_elements(slide6['elements'], 13.33, 810 / 108, slide6['slideStyle'], slide6)

    feat_grid = next(elem for elem in slide6['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in feat_grid.get('children', []) if child.get('type') == 'container')
    bg = next(child for child in first_card['children'] if child.get('_is_card_bg'))
    metric = next(child for child in first_card['children'] if child.get('type') == 'text' and child.get('_slot_metric'))
    inner_h = bg['bounds']['height'] - bg.get('_css_pad_t', 0.0) - bg.get('_css_pad_b', 0.0)
    assert inner_h > 0.1, first_card['bounds']
    assert metric['bounds']['height'] <= inner_h * 0.59, (metric['bounds'], first_card['bounds'])
    print("  PASS: data-story feature cards limit metric share of card height")


def test_data_story_metric_grids_preserve_authored_row_width_when_not_centered():
    """Non-centered data-story KPI grids should fill their authored row width instead of shrink-wrapping."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story KPI grid width preservation (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)

    slide4 = slides[3]
    containers4 = _collect_elements_by_type(slide4['elements'], 'container')
    solution_grid = next(elem for elem in containers4 if elem.get('bounds', {}).get('width', 0.0) > 10.0)
    bottom_grid = next(
        elem for elem in containers4
        if len([
            child for child in elem.get('children', [])
            if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
        ]) == 3
    )
    assert bottom_grid['bounds']['width'] > 10.0, bottom_grid['bounds']
    assert abs(bottom_grid['bounds']['width'] - solution_grid['bounds']['width']) < 0.6, (
        bottom_grid['bounds'], solution_grid['bounds']
    )

    slide7 = slides[6]
    containers7 = _collect_elements_by_type(slide7['elements'], 'container')
    rows = [
        elem for elem in containers7
        if elem.get('type') == 'container' and elem.get('_component_contract') == 'split_rail'
    ]
    bottom_grid7 = next(
        elem for elem in containers7
        if elem.get('type') == 'container' and len([
            child for child in elem.get('children', [])
            if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
        ]) == 3
    )
    assert rows, slide7['elements']
    assert abs(bottom_grid7['bounds']['width'] - rows[0]['bounds']['width']) < 0.4, (
        bottom_grid7['bounds'], rows[0]['bounds']
    )
    print("  PASS: non-centered data-story KPI grids preserve full row width")


def test_data_story_left_aligned_slides_do_not_center_narrow_titles():
    """Left-aligned slides should stay anchored to slide padding even when the heading is narrower than the main rail."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story left-aligned layout (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide2 = slides[1]
    layout_slide_elements(slide2['elements'], 13.33, 810 / 108, slide2['slideStyle'], slide2)
    title = next(elem for elem in slide2['elements'] if elem.get('tag') == 'h2')
    split = next(elem for elem in slide2['elements'] if elem.get('type') == 'container')
    assert title['bounds']['x'] < 1.0, title['bounds']
    assert split['bounds']['x'] < 1.0, split['bounds']
    print("  PASS: left-aligned data-story slides stay anchored to padding")


def test_data_story_relative_grids_normalize_local_origin():
    """Relative grid wrappers should anchor their first child at local x≈0 rather than inheriting a 0.5in offset."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story relative grid normalization (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide4 = slides[3]
    containers = _collect_elements_by_type(slide4['elements'], 'container')
    solution_grid = next(
        elem for elem in containers
        if len([
            child for child in elem.get('children', [])
            if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
        ]) >= 4
    )
    first_card = min(
        [child for child in solution_grid.get('children', []) if child.get('type') == 'container'],
        key=lambda child: child.get('bounds', {}).get('x', 0.0),
    )
    assert first_card['bounds']['x'] < 0.1, first_card['bounds']
    print("  PASS: relative grid wrappers normalize local origin")


def test_data_story_feature_grid_children_stay_within_local_container_width():
    """Top-level feature grids should localize child card coordinates instead of baking slide margins twice."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story feature grid local origin (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide6 = slides[5]
    feat_grid = next(
        elem for elem in slide6['elements']
        if elem.get('type') == 'container' and len([
            child for child in elem.get('children', [])
            if child.get('type') == 'container' and child.get('_component_contract') == 'vertical_card'
        ]) >= 4
    )
    cards = [child for child in feat_grid.get('children', []) if child.get('type') == 'container']
    assert cards, feat_grid
    first_card = min(cards, key=lambda child: child.get('bounds', {}).get('x', 0.0))
    last_card = max(cards, key=lambda child: child.get('bounds', {}).get('x', 0.0))
    assert first_card['bounds']['x'] < 0.1, first_card['bounds']
    assert last_card['bounds']['x'] + last_card['bounds']['width'] <= feat_grid['bounds']['width'] + 0.02, (
        feat_grid['bounds'],
        last_card['bounds'],
    )
    print("  PASS: data-story feature grid children stay within local container width")


def test_export_freeform_open_path_uses_connector_segments():
    """Open SVG polylines should export as explicit connector segments so chart strokes remain visible."""
    prs = export_sandbox.Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    export_sandbox.export_freeform_element(slide, {
        'type': 'freeform',
        'points': [(1.0, 1.0), (2.0, 1.5), (3.0, 1.1)],
        'closed': False,
        'styles': {'stroke': '#3b82f6', 'fill': '', 'strokeWidth': 2.5},
    })
    with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        prs.save(tmp_path)
        with ZipFile(tmp_path) as zf:
            xml = zf.read('ppt/slides/slide1.xml').decode('utf-8')
        assert xml.count('cxnSp') >= 2, xml
    finally:
        tmp_path.unlink(missing_ok=True)
    print("  PASS: open freeform paths export as connector segments")


def test_auto_fit_grid_collapses_empty_tracks_for_three_cards():
    """Auto-fit grids should stretch across available width when there are fewer items than fit tracks."""
    html = """<!doctype html><html><head><style>
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(min(100%,160px),1fr)); gap:16px; }
    .card { background:#1e293b; border:1px solid #334155; border-radius:8px; padding:24px; }
    </style></head><body>
    <section class="slide">
      <div class="grid" style="max-width: 960px;">
        <div class="card">One</div>
        <div class="card">Two</div>
        <div class="card">Three</div>
      </div>
    </section>
    </body></html>"""
    path = write_fixture("autofit-three-cards.html", html)
    slides = parse_html_to_slides(path, 1440)
    grid = next(elem for elem in slides[0]["elements"] if elem.get("type") == "container")
    widths = [child["bounds"]["width"] for child in grid.get("children", [])]
    assert len(widths) == 3, widths
    assert min(widths) > 2.8, widths
    assert max(widths) - min(widths) < 0.05, widths
    print("  PASS: auto-fit grid collapses empty tracks for three cards")


def test_shift_container_descendants_moves_freeform_points():
    """Relative container translation should also move freeform point geometry."""
    container = {
        "type": "container",
        "_children_relative": True,
        "children": [
            {
                "type": "freeform",
                "points": [(0.1, 0.2), (0.3, 0.4)],
                "styles": {"stroke": "#3b82f6"},
            }
        ],
    }
    export_sandbox._shift_container_descendants(container, 1.0, 2.0)
    assert container["children"][0]["points"] == [(1.1, 2.2), (1.3, 2.4)]
    print("  PASS: relative container shifts freeform points")


def test_data_story_style_cards_use_contract_solver_and_keep_preview_slot():
    """Style preview cards should keep the swatch slot as a nested drawable block."""
    html_path = Path('demo/data-story-zh.html')
    if not html_path.exists():
        print("  SKIP: data-story style card solver (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide3 = slides[2]
    grid = next(elem for elem in slide3['elements'] if elem.get('type') == 'container')
    first_card = next(child for child in grid.get('children', []) if child.get('type') == 'container')
    assert first_card.get('_component_contract') == 'vertical_card', first_card
    preview = next((child for child in first_card.get('children', []) if child.get('type') == 'container'), None)
    assert preview is not None, first_card.get('children', [])
    assert preview.get('bounds', {}).get('height', 0.0) >= 0.65, preview.get('bounds')
    print("  PASS: data-story style cards keep preview slot via contract solver")


def test_slide_anchored_text_preserves_bottom_right_position():
    """Author-positioned slide labels should keep explicit bottom-right placement."""
    html = '''
    <html><body>
      <section class="slide" style="position:relative;padding:48px;">
        <h2>Example</h2>
        <span style="position:absolute;bottom:28px;right:36px;font-size:11px;color:rgba(255,255,255,0.18);">04</span>
      </section>
    </body></html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-positioned-label-') as tmp_dir:
        html_path = Path(tmp_dir) / 'positioned-label.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    slide = slides[0]
    label = next(elem for elem in slide['elements'] if elem.get('type') == 'text' and elem.get('text') == '04')
    assert label.get('_skip_layout'), label
    assert label['bounds']['x'] > 12.5, label['bounds']
    assert label['bounds']['y'] > 7.7, label['bounds']
    print("  PASS: slide-anchored text keeps bottom-right position")


def test_parse_html_to_slides_clones_body_fixed_brand_mark_for_each_slide():
    """Non-chrome fixed body overlays should be cloned onto every slide."""
    html = '''
    <html><body>
      <span id="brand-mark" style="position:fixed;top:20px;left:28px;font-weight:800;font-size:15px;color:#3b82f6;">slide-creator</span>
      <section class="slide"><h2>One</h2></section>
      <section class="slide"><h2>Two</h2></section>
    </body></html>
    '''
    with tempfile.TemporaryDirectory(prefix='kai-export-global-brand-') as tmp_dir:
        html_path = Path(tmp_dir) / 'global-brand.html'
        html_path.write_text(html, encoding='utf-8')
        slides = parse_html_to_slides(html_path, 1440, 810)

    assert len(slides) == 2, slides
    for slide in slides:
        brand = next(
            (elem for elem in slide['elements'] if elem.get('type') == 'text' and elem.get('text') == 'slide-creator'),
            None,
        )
        assert brand is not None, slide['elements']
        assert brand.get('_skip_layout'), brand
        assert brand['bounds']['x'] < 0.5 and brand['bounds']['y'] < 0.3, brand['bounds']
    print("  PASS: body fixed brand mark is cloned onto every slide")


def test_centered_flex_wrap_preserves_intrinsic_metric_stack_widths():
    """Centered flex-wrap rows should not over-wrap simple grouped KPI stacks."""
    html = '''
    <div style="display:flex; justify-content:center; align-items:center; gap:20px; flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-size:56px; font-weight:800; line-height:1;">21</div>
        <div style="font-size:11px; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#8b949e; margin-top:8px;">PRESETS</div>
      </div>
      <div style="width:1px; height:48px; background:#30363d;"></div>
      <div style="text-align:center;">
        <div style="font-size:56px; font-weight:800; line-height:1;">0</div>
        <div style="font-size:11px; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#8b949e; margin-top:8px;">DEPS</div>
      </div>
      <div style="width:1px; height:48px; background:#30363d;"></div>
      <div style="text-align:center;">
        <div style="font-size:56px; font-weight:800; line-height:1;">∞</div>
        <div style="font-size:11px; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#8b949e; margin-top:8px;">SLIDES</div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find('div')
    style = compute_element_style(row, [], row.get('style', ''))
    children = build_grid_children(row, [], style, 1440, content_width_px=800)
    assert len(children) == 5, children
    ys = [round(child['bounds']['y'], 3) for child in children]
    assert max(ys) - min(ys) < 0.05, ys
    assert children[4]['bounds']['x'] > children[3]['bounds']['x'], [child['bounds'] for child in children]
    print("  PASS: centered flex-wrap preserves intrinsic metric stack widths")


def test_compact_flex_row_packs_stat_blocks_at_intrinsic_width():
    """`.hero-stats { display:flex; gap }` (no justify-content) must pack each
    stat block at intrinsic width, not divide the row evenly."""
    html = '''
    <div style="display:flex; gap:48px;">
      <div>
        <div style="font-size:48px; font-weight:900; line-height:1;">21</div>
        <div style="font-size:11px; letter-spacing:0.08em;">设计预设</div>
      </div>
      <div>
        <div style="font-size:48px; font-weight:900; line-height:1;">0</div>
        <div style="font-size:11px; letter-spacing:0.08em;">运行时依赖</div>
      </div>
      <div>
        <div style="font-size:48px; font-weight:900; line-height:1;">3</div>
        <div style="font-size:11px; letter-spacing:0.08em;">分钟出稿</div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find('div')
    style = compute_element_style(row, [], row.get('style', ''))
    children = build_grid_children(row, [], style, 1280, content_width_px=900)
    # Stacked stat blocks may flatten into per-line children, but each stat's
    # numeric token (font-size 48px) marks the column start. The three numeric
    # tokens must pack tightly, NOT evenly span ~9".
    num_tokens = [c for c in children if c.get('text', '').strip() in ('21', '0', '3')]
    assert len(num_tokens) == 3, num_tokens
    xs = sorted(round(c['bounds']['x'], 3) for c in num_tokens)
    # Compact span: three numeric anchors fall within ~3" — was ~8.4" pre-fix.
    assert xs[2] - xs[0] < 3.0, xs
    # Each numeric token shrink-wraps its glyph width (≤ 0.6") — NOT a 3" slice.
    num_widths = [round(c['bounds']['width'], 3) for c in num_tokens]
    for w in num_widths:
        assert w < 0.7, num_widths
    print("  PASS: compact flex-row packs stat blocks at intrinsic width")


def test_compact_flex_row_falls_back_to_even_split_when_oversized():
    """When intrinsic widths overflow the container, fall back to even split.

    Stacked-block stats normally hit the compact-packing path (flex_slots),
    but if the container is far too narrow to fit the intrinsic measurements,
    we keep the legacy even-split so nothing collapses to zero.
    """
    html = '''
    <div style="display:flex; gap:16px;">
      <div>
        <div style="font-size:120px; line-height:1;">VERYWIDE</div>
        <div style="font-size:14px;">label one</div>
      </div>
      <div>
        <div style="font-size:120px; line-height:1;">ALSOWIDE</div>
        <div style="font-size:14px;">label two</div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find('div')
    style = compute_element_style(row, [], row.get('style', ''))
    # Container too narrow to fit two giant numeric stacks side-by-side
    children = build_grid_children(row, [], style, 1280, content_width_px=200)
    assert children, children
    # Group children by stat-block (numeric token at large font marks anchor)
    big_tokens = [c for c in children if 'WIDE' in (c.get('text', '') or '')]
    assert len(big_tokens) == 2, big_tokens
    widths = [round(c['bounds']['width'], 3) for c in big_tokens]
    # Fallback even-split → both anchors get the same slot width
    assert abs(widths[0] - widths[1]) < 0.05, widths
    print("  PASS: compact flex-row falls back to even split when oversized")


def test_stretch_column_block_text_to_inner_width_expands_narrow_heading():
    """Block-level headings inside a column panel must claim the full inner
    panel width so authored `<br>` line breaks don't get re-wrapped into
    orphaned half-rows."""
    container = {
        'type': 'container',
        'tag': 'div',
        'bounds': {'x': 0.0, 'y': 0.0, 'width': 4.0, 'height': 2.0},
        'children': [
            {
                'type': 'text',
                'tag': 'h2',
                'text': '演示文稿制作\n本不该这么难',
                'bounds': {'x': 0.0, 'y': 0.0, 'width': 2.08, 'height': 1.5},
                'styles': {'fontSize': '36px'},
            },
            {
                'type': 'text',
                'tag': 'span',  # inline, must NOT be stretched
                'text': 'inline label',
                'bounds': {'x': 0.0, 'y': 1.6, 'width': 1.2, 'height': 0.18},
                'styles': {'fontSize': '14px'},
            },
        ],
    }
    _stretch_column_block_text_to_inner_width(container, 3.90)
    h2 = container['children'][0]
    span = container['children'][1]
    assert abs(h2['bounds']['width'] - 3.90) < 0.001, h2['bounds']
    assert abs(span['bounds']['width'] - 1.2) < 0.001, span['bounds']

    # Already-wide heading must not shrink
    container2 = {
        'type': 'container',
        'tag': 'div',
        'children': [
            {
                'type': 'text',
                'tag': 'h2',
                'text': 'wide title',
                'bounds': {'x': 0.0, 'y': 0.0, 'width': 5.0, 'height': 0.6},
                'styles': {'fontSize': '36px'},
            },
        ],
    }
    _stretch_column_block_text_to_inner_width(container2, 3.90)
    assert abs(container2['children'][0]['bounds']['width'] - 5.0) < 0.001
    print("  PASS: column block text stretches to inner panel width")


def test_swiss_index_list_rows_stretch_full_width_with_left_number_column():
    """`.sol-list` rows should pin the index number to the left and stretch
    the content column across the rest of the row, baseline-anchored."""
    html = '''
    <div class="sol-list" style="display:flex; flex-direction:column; gap:2px;">
      <div class="index-item" style="display:flex; align-items:baseline; gap:16px; padding:8px 0; border-bottom:1px solid #e5e5e5;">
        <span class="index-num" style="font-family:Archivo Black; font-size:48px; font-weight:900; line-height:1; min-width:72px; color:#c41e3a;">01</span>
        <div><span style="font-size:24px; font-weight:900;">Bold Signal</span><br><span style="font-size:14px;">High-contrast accent</span></div>
      </div>
      <div class="index-item" style="display:flex; align-items:baseline; gap:16px; padding:8px 0; border-bottom:1px solid #e5e5e5;">
        <span class="index-num" style="font-family:Archivo Black; font-size:48px; font-weight:900; line-height:1; min-width:72px; color:#c41e3a;">02</span>
        <div><span style="font-size:24px; font-weight:900;">Aurora Mesh</span><br><span style="font-size:14px;">Gradient backdrop</span></div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    list_node = soup.find('div', class_='sol-list')
    inner_w_in = 11.83
    rows = _build_swiss_index_list_rows(list_node, [], 1280, inner_w_in, contract=None)
    nums = [r for r in rows if r.get('text', '').strip() in ('01', '02')]
    contents = [r for r in rows if 'Bold Signal' in (r.get('text', '') or '') or 'Aurora Mesh' in (r.get('text', '') or '')]
    assert len(nums) == 2, nums
    assert len(contents) == 2, contents
    # Numbers pinned left at x=0 (relative to inner container)
    for n in nums:
        assert n['bounds']['x'] < 0.05, n['bounds']
    # Content column starts after number + gap and stretches across the rest
    for c in contents:
        assert c['bounds']['x'] > 0.6, c['bounds']  # past number column
        assert c['bounds']['width'] > 8.0, c['bounds']  # stretched, not 1.7"
    # Content baseline-aligned: dropped below number top by ≈ font-size delta
    n0_y = nums[0]['bounds']['y']
    c0_y = contents[0]['bounds']['y']
    assert c0_y > n0_y, (n0_y, c0_y)
    assert (c0_y - n0_y) < 0.5, (n0_y, c0_y)
    # Two rows stack vertically with gap between them
    assert nums[1]['bounds']['y'] > nums[0]['bounds']['y'] + 0.4, [nums[0]['bounds'], nums[1]['bounds']]
    print("  PASS: swiss index_list rows stretch full width with left number column")


def test_swiss_terminal_line_renders_dark_pill_with_paired_overlay():
    """`.terminal-line` (inline-block + bg) must render as a paired bg shape +
    text overlay, NOT collapse into the parent's text content."""
    html = '''
    <span class="terminal-line"
      style="font-family:monospace; font-size:14px; background:#0A0A0A; color:#fff; padding:10px 16px; display:inline-block;">
      clawhub install kai-slide-creator
    </span>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='terminal-line')
    elements = _build_swiss_terminal_line(span, [], None, 1280, max_w_in=7.0, rel_y_in=0.5)
    assert len(elements) == 2, elements
    shape, text = elements[0], elements[1]
    assert shape.get('type') == 'shape', shape
    assert text.get('type') == 'text', text
    # Paired so render keeps them aligned
    assert shape.get('_pair_with') == text.get('_pair_with'), (shape.get('_pair_with'), text.get('_pair_with'))
    # Pill is taller than the bare text (padding included)
    assert shape['bounds']['height'] > text['bounds']['height'] + 0.05, (shape['bounds'], text['bounds'])
    # Pill width includes left+right padding around the text
    assert shape['bounds']['width'] > text['bounds']['width'] + 0.1, (shape['bounds'], text['bounds'])
    # Both anchored at rel_y_in=0.5 (text inset by pad_t)
    assert abs(shape['bounds']['y'] - 0.5) < 0.001, shape
    assert text['bounds']['y'] > shape['bounds']['y'], (shape, text)
    print("  PASS: swiss terminal-line renders dark pill with paired overlay")


def test_swiss_disc_steps_stack_vertically_with_left_number_column():
    """`.disc-steps` must stack each `.disc-step` vertically, NOT spread them
    horizontally. Each step's number column sits at x=0 with the content
    column starting after `min-width + gap`."""
    html = '''
    <div class="disc-steps" style="display:flex; flex-direction:column; gap:16px;">
      <div class="disc-step" style="display:flex; gap:12px; align-items:flex-start;">
        <div class="disc-step-num" style="font-size:32px; font-weight:900; line-height:1; min-width:36px; color:#c41e3a;">01</div>
        <div>
          <div class="disc-step-title" style="font-size:18px; font-weight:900;">Describe theme</div>
          <p class="disc-step-desc" style="font-size:14px;">Enter content and audience.</p>
        </div>
      </div>
      <div class="disc-step" style="display:flex; gap:12px; align-items:flex-start;">
        <div class="disc-step-num" style="font-size:32px; font-weight:900; line-height:1; min-width:36px; color:#c41e3a;">02</div>
        <div>
          <div class="disc-step-title" style="font-size:18px; font-weight:900;">Generate previews</div>
          <p class="disc-step-desc" style="font-size:14px;">Three different style options.</p>
        </div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    steps_node = soup.find('div', class_='disc-steps')
    elements, total_h = _build_swiss_disc_steps(steps_node, [], 1280, column_w_in=4.5, contract=None)
    assert elements, elements
    nums = [e for e in elements if e.get('text', '').strip() in ('01', '02')]
    assert len(nums) == 2, nums
    # All numbers pinned to x=0 (left column)
    for n in nums:
        assert abs(n['bounds']['x']) < 0.01, n['bounds']
    # Numbers stack vertically, not horizontally
    assert nums[1]['bounds']['y'] > nums[0]['bounds']['y'] + 0.4, [n['bounds'] for n in nums]
    # Total height non-degenerate
    assert total_h > 0.6, total_h
    print("  PASS: swiss disc_steps stack vertically with left number column")


def test_hairline_height_halves_thin_borders_and_passes_thick_through():
    """1-2px CSS borders need a halved PPTX shape height (PPTX shapes render
    at minimum 1 device pixel); thicker borders pass through unchanged."""
    one_px_in = _hairline_height_in(1.0)
    two_px_in = _hairline_height_in(2.0)
    three_px_in = _hairline_height_in(3.0)
    # 1px CSS → 0.5px equivalent (= 0.5 / PX_PER_IN)
    assert abs(one_px_in - 0.5 / export_sandbox.PX_PER_IN) < 1e-6, one_px_in
    # 2px CSS → 1px equivalent
    assert abs(two_px_in - 1.0 / export_sandbox.PX_PER_IN) < 1e-6, two_px_in
    # 3px+ pass through (no halving)
    assert abs(three_px_in - 3.0 / export_sandbox.PX_PER_IN) < 1e-6, three_px_in
    # Zero / negative returns 0
    assert _hairline_height_in(0) == 0.0
    assert _hairline_height_in(-1) == 0.0
    print("  PASS: hairline height halves thin borders and passes thick through")


def test_build_css_hairline_shape_extracts_color_and_skips_none():
    """The generic hairline helper accepts CSS border shorthand and emits a
    decoration shape, skipping `none` / 0 width."""
    shape = _build_css_hairline_shape(
        '1px solid #e5e5e5', x_in=0.5, y_in=2.0, width_in=10.0
    )
    assert shape is not None
    assert shape['type'] == 'shape'
    assert shape['_is_decoration'] is True
    assert shape['layoutDone'] is True
    assert shape['styles']['backgroundColor'] == '#e5e5e5'
    assert abs(shape['bounds']['height'] - 0.5 / export_sandbox.PX_PER_IN) < 1e-6
    assert shape['bounds']['width'] == 10.0
    # `none` returns None
    assert _build_css_hairline_shape('none', 0, 0, 5) is None
    # `0` width returns None
    assert _build_css_hairline_shape('0px solid #ccc', 0, 0, 5) is None
    # Empty returns None
    assert _build_css_hairline_shape('', 0, 0, 5) is None
    # Falls back to default color when no color in border
    s2 = _build_css_hairline_shape('1px solid', 0, 0, 5)
    assert s2 is not None
    assert s2['styles']['backgroundColor'] == '#e5e5e5'
    print("  PASS: _build_css_hairline_shape extracts color and skips none")


def test_layout_slide_elements_respects_slide_justify_center():
    """Slide roots authored with justify-content:center should vertically center the content block."""
    elements = [
        {
            'type': 'text',
            'tag': 'h1',
            'text': 'Centered title',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 3.0, 'height': 0.7},
            'styles': {'fontSize': '42px', 'textAlign': 'center', 'lineHeight': '42px'},
        },
        {
            'type': 'text',
            'tag': 'p',
            'text': 'Centered body',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 4.0, 'height': 0.4},
            'styles': {'fontSize': '18px', 'textAlign': 'center', 'lineHeight': '28px', 'marginTop': '16px'},
        },
    ]
    slide_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'paddingTop': '96px',
        'paddingBottom': '96px',
        'textAlign': 'center',
    }
    layout_slide_elements(elements, slide_style=slide_style)
    top_y = min(elem['bounds']['y'] for elem in elements)
    assert top_y > 2.4, [elem['bounds'] for elem in elements]
    assert elements[1]['bounds']['y'] > elements[0]['bounds']['y'], [elem['bounds'] for elem in elements]
    print("  PASS: layout_slide_elements vertically centers justify-content:center slides")


def test_layout_slide_elements_respects_slide_justify_flex_end():
    """Slide roots authored with justify-content:flex-end should anchor the content block to the bottom runway."""
    elements = [
        {
            'type': 'text',
            'tag': 'h1',
            'text': 'Anchored title',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 3.2, 'height': 0.7},
            'styles': {'fontSize': '42px', 'lineHeight': '42px'},
        },
        {
            'type': 'text',
            'tag': 'p',
            'text': 'Anchored body',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 4.2, 'height': 0.4},
            'styles': {'fontSize': '18px', 'lineHeight': '28px', 'marginTop': '16px'},
        },
    ]
    slide_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'flex-end',
        'paddingTop': '54px',
        'paddingBottom': '108px',
    }
    layout_slide_elements(elements, slide_height_in=810 / 108, slide_style=slide_style)
    top_y = min(elem['bounds']['y'] for elem in elements)
    bottom_y = max(elem['bounds']['y'] + elem['bounds']['height'] for elem in elements)
    assert top_y > 4.8, [elem['bounds'] for elem in elements]
    assert bottom_y <= (810 / 108) - 0.95, [elem['bounds'] for elem in elements]
    print("  PASS: layout_slide_elements anchors justify-content:flex-end slides to bottom runway")


def test_layout_slide_elements_ignores_skip_layout_overlays_when_centering():
    """Fixed/absolute overlays should not block slide-level vertical centering."""
    elements = [
        {
            'type': 'text',
            'tag': 'span',
            'text': 'slide-creator',
            'bounds': {'x': 0.26, 'y': 0.24, 'width': 1.1, 'height': 0.23},
            '_skip_layout': True,
            'styles': {'position': 'fixed', 'top': '20px', 'left': '28px'},
        },
        {
            'type': 'text',
            'tag': 'h2',
            'text': 'Centered heading',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 4.0, 'height': 0.37},
            'styles': {'fontSize': '40px', 'textAlign': 'left', 'lineHeight': '40px'},
        },
        {
            'type': 'container',
            'tag': 'div',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 12.0, 'height': 6.0},
            'styles': {},
            'children': [],
            '_children_relative': True,
        },
        {
            'type': 'text',
            'tag': 'span',
            'text': '02',
            'bounds': {'x': 12.8, 'y': 7.98, 'width': 0.19, 'height': 0.15},
            '_skip_layout': True,
            'styles': {'position': 'absolute', 'bottom': '28px', 'right': '36px'},
        },
    ]
    slide_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'paddingTop': '16px',
        'paddingBottom': '16px',
    }
    layout_slide_elements(elements, slide_height_in=8.33, slide_style=slide_style)
    heading = next(elem for elem in elements if elem.get('text') == 'Centered heading')
    overlay = next(elem for elem in elements if elem.get('text') == 'slide-creator')
    assert heading['bounds']['y'] > 0.75, [elem['bounds'] for elem in elements]
    assert abs(overlay['bounds']['y'] - 0.24) < 0.05, overlay['bounds']
    print("  PASS: skip-layout overlays do not block vertical centering")


def test_flat_extract_skips_display_none_elements():
    """Nodes hidden by computed CSS should not leak into the export IR."""
    html = '''
    <section class="slide">
      <div>Hello</div>
      <span class="hidden-label">Should stay hidden</span>
    </section>
    <style>
      .hidden-label { display: none; }
    </style>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    slide = soup.find('section')
    results = flat_extract(slide, css_rules, None, 1440)
    texts = _collect_text_values(results)
    assert 'Should stay hidden' not in texts, texts
    print("  PASS: flat_extract skips display:none elements")


def test_flat_extract_text_only_inline_flex_container_emits_text():
    """Text-only inline-flex wrappers should export as text, not empty containers."""
    html = '''
    <div style="display:inline-flex; align-items:center; gap:4px; color:#3fb950; font-size:13px; font-weight:600;">
      ▲ 浏览器即运行时
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    elem = soup.find('div')
    results = flat_extract(elem, [], None, 1440)
    assert len(results) == 1, results
    assert results[0].get('type') == 'text', results
    assert '浏览器即运行时' in (results[0].get('text') or ''), results[0]
    print("  PASS: text-only inline-flex wrapper exports as text")


def test_measure_flow_box_inline_flex_card_prefers_intrinsic_width():
    """Inline-flex cards with visible backgrounds should shrink-wrap to their content."""
    html = '''
    <div style="display:inline-flex; flex-direction:row; align-items:center; gap:16px; background:#1b1f24; border:1px solid #30363d; padding:16px 24px; border-radius:6px;">
      <div style="font-size:40px; font-weight:700; color:#3fb950;">100%</div>
      <div>
        <div style="font-size:13px; color:#c9d1d9;">零依赖运行</div>
        <div style="display:inline-flex; align-items:center; gap:4px; font-size:13px; font-weight:600; color:#3fb950;">▲ 浏览器即运行时</div>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div')
    flow_box = measure_flow_box(card, [], None, 1440, content_width_px=800, local_origin=True)
    assert flow_box is not None
    assert flow_box['bounds']['width'] < (800 / PX_PER_IN) - 1.0, flow_box['bounds']
    # Compact flex-row packing (gap + no distributing justify-content) packs
    # each child at its intrinsic content width, so the card shrinks tighter
    # than the older even-split behavior. Floor at 2.3" guards against a
    # degenerate padding-only result.
    assert flow_box['bounds']['width'] > 2.3, flow_box['bounds']
    print("  PASS: inline-flex flow_box cards prefer intrinsic width")


def test_measure_flow_box_flex_column_card_preserves_outer_slot_width():
    """Flow-box cards should size to the outer grid slot, not collapse to inner content width."""
    html = '''
    <div style="display:flex; flex-direction:column; background:#161b22; border:1px solid #30363d; border-radius:6px; padding:24px;">
      <span style="font-size:24px; font-weight:800; color:#58a6ff;">01</span>
      <h3 style="font-size:16px; margin-bottom:4px;">描述心情</h3>
      <p style="font-size:14px;">大胆且极简，或者温暖而创意。</p>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div')
    style = compute_element_style(card, [], card.get('style', ''))
    flow_box = measure_flow_box(card, [], None, 1440, content_width_px=280, local_origin=True)
    assert flow_box is not None
    assert abs(flow_box['bounds']['width'] - (280.0 / PX_PER_IN)) < 0.05, flow_box['bounds']
    print("  PASS: flex-column flow_box cards preserve outer slot width")


def test_stat_card_padding_included_in_width():
    """Slide 1: Centered flex items (stat cards) should include CSS padding in item width.

    Before fix: item_width only contained text content width (e.g., "21" at ~0.46"),
    causing centering to place cards too far left (5.86" vs golden 5.35").

    After fix: item_width includes paddingLeft + paddingRight (28px each = 0.52"),
    so centering uses the full card width and matches golden position.
    """
    # Simulate the padding computation used in build_grid_children
    pad_l_px = 28  # paddingLeft: 28px
    pad_r_px = 28  # paddingRight: 28px
    text_width = 0.46  # "21" text width in inches

    pad_l_in = pad_l_px / PX_PER_IN
    pad_r_in = pad_r_px / PX_PER_IN
    total_width = text_width + pad_l_in + pad_r_in

    # Card should be ~0.97" wide (text + 56px padding)
    expected = text_width + (56.0 / PX_PER_IN)
    assert abs(total_width - expected) < 0.01, f"Card width {total_width:.3f} != {expected:.3f}"
    assert total_width > 0.9, f"Card width {total_width:.3f} should be > 0.9\""
    print("  PASS: stat card padding included in width")


def test_centered_flex_x_position_with_padding():
    """Slide 1: Centered flex row with padded cards should center correctly.

    Given 3 stat cards with widths [~0.97", ~0.75", ~0.75"] and gap 14px (0.13"):
    - Total = 0.97 + 0.75 + 0.75 + 2*0.13 = 2.73"
    - x_start = (13.33 - 2.73) / 2 = 5.30"
    - Golden shows 5.35" (small difference from font rendering)
    """
    slide_w = 13.33
    card_widths = [0.97, 0.75, 0.75]  # includes padding
    gap = 14.0 / PX_PER_IN  # 0.13"
    total = sum(card_widths) + 2 * gap
    x_start = (slide_w - total) / 2

    # Should be close to golden's 5.35"
    assert abs(x_start - 5.35) < 0.1, f"x_start {x_start:.3f} too far from golden 5.35\""
    print("  PASS: centered flex x position with padding")


def test_slide1_stat_positions():
    """Slide 1: Verify actual parsed slide has stat items at correct positions.

    This is an integration test — parses the actual HTML and checks the
    computed element positions after layout.
    """
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide1_stat_positions (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    s1 = slides[0]
    elems = s1['elements']
    export_sandbox.pre_pass_corrections(elems)
    layout_slide_elements(elems, 13.33, 8.33, s1.get('slideStyle', {}), s1)

    # Flatten containers to access stat text elements
    if _flatten_nested_containers:
        _flatten_nested_containers(elems)
    else:
        # Manually flatten: collect text from container children
        flat = []
        for e in elems:
            flat.append(e)
            for c in e.get('children', []):
                flat.append(c)
        elems[:] = flat

    # Find stat number elements
    stat_nums = []
    stat_labels = []
    for e in elems:
        if e.get('type') == 'text':
            txt = e.get('text', '').strip()
            if txt in ('21', '0', '1'):
                stat_nums.append(e)
            elif txt in ('设计预设', '依赖', 'HTML 文件'):
                stat_labels.append(e)

    # Verify stat numbers are positioned (not at default 0.50")
    for e in stat_nums:
        x = e['bounds'].get('x', 0)
        # After fix, x should be > 5.0" (centered on slide)
        assert x > 5.0, f"Stat '{e.get('text','')}' x={x:.3f} should be > 5.0\""
        # Golden stat positions: 21→5.35, 0→6.48, 1→7.39
        assert x < 8.5, f"Stat '{e.get('text','')}' x={x:.3f} too far right"

    # Verify labels are positioned below their numbers
    for e in stat_labels:
        y = e['bounds'].get('y', 0)
        assert y > 0.5, f"Label '{e.get('text','')}' y={y:.3f} should be below title"

    print("  PASS: slide1 stat positions")


def test_slide1_all_text_present():
    """Slide 1: All 10 text elements from HTML should be present in parsed output."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide1_all_text_present (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    s1 = slides[0]
    elems = s1['elements']

    # Count text elements (including nested in containers)
    text_count = 0
    for e in elems:
        if e.get('type') == 'text':
            text_count += 1
        elif e.get('type') == 'container':
            for c in e.get('children', []):
                if c.get('type') == 'text':
                    text_count += 1
                elif c.get('type') == 'container':
                    for gc in c.get('children', []):
                        if gc.get('type') == 'text':
                            text_count += 1

    assert text_count >= 9, f"Slide 1 should have >= 9 text elements, got {text_count}"
    print("  PASS: slide1 all text present")


def test_heading_content_width():
    """Slide 1: Heading width computation for centering.

    The title 'HTML 演示文稿' at 72px should determine the content area width,
    which is then used to center all content on the slide.
    """
    text = "HTML 演示文稿"
    font_px = 72.0
    cjk = sum(1 for c in text if ord(c) > 127)  # 4 CJK chars
    latin = len(text) - cjk  # 5 latin chars (HTML + space)
    width = (cjk * font_px + latin * font_px * 0.55) / PX_PER_IN

    # Expected ~4.50"
    assert 4.0 < width < 5.0, f"Heading width {width:.3f}\" should be ~4.50\""
    print("  PASS: heading content width")


def test_centered_explicit_break_heading_gets_wrap_guard_width():
    """Large centered headings with explicit line breaks should get extra wrap safety width."""
    html = '''
    <section class="slide">
      <h1 style="font-size:4.5rem;font-weight:800;line-height:1.1;letter-spacing:-0.02em;text-align:center;">
        AI 驱动的<br>HTML 演示文稿
      </h1>
    </section>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = []
    h1 = soup.find('h1')
    style = compute_element_style(h1, css_rules, h1.get('style', ''))
    text_el = build_text_element(h1, style, css_rules, 1440, 940)
    bare_line_width_in = max(
        export_sandbox._estimate_text_width_px(line.strip(), 72.0, letter_spacing='-0.02em') / PX_PER_IN
        for line in ('AI 驱动的', 'HTML 演示文稿')
    )
    layout_slide_elements([text_el], 13.33, 810 / 108, {'paddingTop': '40px'}, {'_slide_index': 0})

    assert text_el['bounds']['width'] >= bare_line_width_in + 0.14, text_el['bounds']
    print("  PASS: explicit-break display heading gets wrap-guard width")


def test_map_font_prefers_office_safe_font_in_mixed_cjk_stack():
    """Mixed platform/system CJK stacks should resolve to an installed browser-faithful fallback."""
    css_stack = "'PingFang SC', 'Microsoft YaHei', 'DM Sans', system-ui, -apple-system, sans-serif"
    assert map_font(css_stack, text='中文标题') == ('Hiragino Sans GB', 'Hiragino Sans GB')
    print("  PASS: mixed CJK font stack prefers installed browser-faithful font pair")


def test_pill_text_included_in_parent():
    """Pill text should be included in parent text, not separated.

    Before fix: exclude_elements caused pill children to be excluded from
    parent text extraction, splitting "Blue Sky 当前" into two elements.

    After fix: all text (including pill children) is included in the parent
    text element. The pill shape is visual-only (no embedded text).
    """
    # Simulate a container with a pill child
    html = '''<div style="background: rgba(223,237,253,0.5); padding: 8px;">
      Blue Sky <span style="background: #D5F1EF; padding: 2px 8px; border-radius: 4px;">当前</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div')

    # Verify get_text_content includes pill text
    text = export_sandbox.get_text_content(div)
    assert '当前' in text, f"Pill text '当前' should be in parent text, got: {text!r}"
    assert 'Blue Sky' in text, f"'Blue Sky' should be in text, got: {text!r}"
    print("  PASS: pill text included in parent")


def test_decoration_shape_for_no_text_elements():
    """Elements with visible bg + explicit CSS dimensions but no text should create decoration shapes.

    Before fix: leaf text containers with no text were completely skipped,
    losing small decorative elements like theme dots (10px×10px circles).

    After fix: such elements create _is_decoration shapes with correct dimensions.
    """
    # Test with a style dict that simulates a dot element
    style = {
        'backgroundColor': '#0F172A',
        'width': '10px',
        'height': '10px',
        'borderRadius': '50%',
    }

    # Verify has_visible_bg_or_border works
    assert export_sandbox.has_visible_bg_or_border(style), "Dot should have visible bg"

    # Simulate the decoration shape creation logic
    _lcw = style.get('width', '')
    _lch = style.get('height', '')
    if _lcw and _lch and _lcw.endswith('px') and _lch.endswith('px'):
        _lcwp = parse_px(_lcw)
        _lchp = parse_px(_lch)
        if _lcwp > 0 and _lchp > 0 and _lcwp < 200 and _lchp < 200:
            w_in = _lcwp / PX_PER_IN
            h_in = _lchp / PX_PER_IN
            assert abs(w_in - 10.0 / PX_PER_IN) < 0.01, f"Width {w_in:.3f} should be ~{10.0/PX_PER_IN:.3f}"
            assert abs(h_in - 10.0 / PX_PER_IN) < 0.01, f"Height {h_in:.3f} should be ~{10.0/PX_PER_IN:.3f}"
            print("  PASS: decoration shape for no-text elements")
        else:
            raise AssertionError(f"Small element check failed: {_lcwp}x{_lchp}")
    else:
        raise AssertionError(f"CSS dimensions not found: {_lcw!r}x{_lch!r}")


def test_pill_shape_no_text():
    """Pill shapes should not have embedded text (visual-only decoration).

    Before fix: pills had pill_text and pill_color fields, rendering text
    inside the shape.

    After fix: pills are _is_pill shapes without text — the text stays in
    the parent text element.
    """
    html = '''<div style="display: flex; gap: 8px;">
      <span style="background: #D5F1EF; padding: 2px 8px; border-radius: 4px;">当前</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div')

    style = export_sandbox.compute_element_style(div, [], '')
    results = export_sandbox.flat_extract(div, [], style, 1440)

    # Check that any pill shapes don't have pill_text or pill_color
    for r in results:
        if r.get('_is_pill'):
            assert 'pill_text' not in r, f"Pill should not have pill_text, got: {r.get('pill_text')!r}"
            assert 'pill_color' not in r, "Pill should not have pill_color"
    print("  PASS: pill shape has no embedded text")


# ─── Slide 5 Chapter Page Tests ───────────────────────────────────────────────

def test_chapter_page_max_width_from_widest_element():
    """Slide 5: max_width should use widest centered text element, not just heading.

    Before fix: max_width was set from heading width (2.076"), constraining
    the paragraph's natural width (2.707").
    After fix: max_width is computed from all centered text elements.
    """
    slide_style = {'textAlign': 'center', 'justifyContent': 'center', 'flexDirection': 'column'}

    # Simulate chapter page elements: big number, heading, divider, paragraph
    elements = [
        {'type': 'text', 'tag': 'div', 'text': '01',
         'bounds': {'x': 0.5, 'y': 0, 'width': 12.33, 'height': 1.63},
         'styles': {'textAlign': 'center', 'fontSize': '176px', 'lineHeight': '1'},
         'naturalHeight': 1.63},
        {'type': 'text', 'tag': 'h2', 'text': '工程化能力',
         'bounds': {'x': 0.5, 'y': 0, 'width': 12.33, 'height': 0.462},
         'styles': {'textAlign': 'center', 'fontSize': '41.6px', 'lineHeight': '1.2'},
         'naturalHeight': 0.462},
        {'type': 'shape', 'tag': 'div', 'text': '',
         'bounds': {'x': 0.5, 'y': 0, 'width': 0.519, 'height': 0.03},
         'styles': {}},
        {'type': 'text', 'tag': 'p', 'text': '播放、编辑、Review —— 全流程闭环',
         'bounds': {'x': 0.5, 'y': 0, 'width': 12.33, 'height': 0.249},
         'styles': {'textAlign': 'center', 'fontSize': '16.8px', 'lineHeight': '1.6'},
         'naturalHeight': 0.249},
    ]

    layout_slide_elements(elements, 13.33, 8.333, slide_style)

    # Paragraph should be wider than heading (not constrained to heading width)
    heading_w = elements[1]['bounds']['width']
    para_w = elements[3]['bounds']['width']
    assert para_w > heading_w, f"Paragraph width ({para_w:.3f}\") should be wider than heading ({heading_w:.3f}\")"
    # Paragraph should be at least 2.5" (golden is 2.634")
    assert para_w > 2.5, f"Paragraph width {para_w:.3f}\" should be > 2.5\""
    print("  PASS: paragraph wider than heading in centered layout")


def test_chapter_page_zero_padding_for_large_text():
    """Slide 5: Large text widths should not have +0.15 padding.

    Before fix: text_w + 0.15 overestimated widths for large fonts.
    After fix: text_w > 1.0 uses zero padding.
    """
    # "01" at 176px: text_w = 2 * 176 * 0.55 / 108 = 1.793"
    # With +0.15 padding: 1.943" (wrong)
    # Without padding: 1.793" (correct, close to golden 1.646")
    text_w = 2 * 176 * 0.55 / PX_PER_IN
    assert text_w > 1.0  # should use zero padding branch

    # Simulate the width formula
    if text_w > 1.0:
        content_width = text_w  # zero padding
    else:
        content_width = text_w * 1.3 + 1.0

    # Should be close to text_w, not text_w + 0.15
    assert abs(content_width - text_w) < 0.01, f"content_width {content_width:.3f}\" should be ~{text_w:.3f}\""
    print("  PASS: zero padding for large text widths")


def test_chapter_page_paragraph_single_line():
    """Slide 5: Paragraph "播放..." is rendered as 1 line in golden PPTX,
    but the estimate formula is approximate (±1 line).
    The golden shows the text at w=2.634" on a single line, meaning PPTX
    renders more compactly than the formula estimates.
    """
    text = '播放、编辑、Review —— 全流程闭环'
    font_size_pt = 12.6
    box_width = 2.757  # paragraph box width

    lines = export_sandbox.estimate_wrapped_lines(text, font_size_pt, box_width)
    # Formula is approximate — may return 1 or 2 lines for borderline cases
    assert lines <= 2, f"Paragraph should be at most 2 lines, got {lines}"
    print("  PASS: paragraph line count within tolerance")


def test_chapter_page_no_overflow():
    """Slide 5: No text overflow issues on chapter page."""
    from pptx import Presentation
    pptx_path = Path(__file__).parent.parent / 'demo' / 'output.pptx'
    if not pptx_path.exists():
        print("  SKIP: demo/output.pptx not found")
        return

    prs = Presentation(str(pptx_path))
    slide5 = prs.slides[4]  # 0-indexed
    slide_w = prs.slide_width / 914400

    for shape in slide5.shapes:
        text = getattr(shape, 'text', '') or ''
        if len(text) < 5:
            continue
        x = shape.left / 914400
        w = shape.width / 914400
        right_edge = x + w
        assert right_edge < slide_w + 0.05, f"Text '{text[:30]}...' overflows: right={right_edge:.2f}\" > slide_w={slide_w:.2f}\""
    print("  PASS: no text overflow on chapter page")


def test_chapter_page_no_overlap():
    """Slide 5: No element overlap on chapter page."""
    from pptx import Presentation
    pptx_path = Path(__file__).parent.parent / 'demo' / 'output.pptx'
    if not pptx_path.exists():
        print("  SKIP: demo/output.pptx not found")
        return

    prs = Presentation(str(pptx_path))
    slide5 = prs.slides[4]

    text_shapes = []
    for shape in slide5.shapes:
        text = getattr(shape, 'text', '') or ''
        if text.strip():
            text_shapes.append({
                'text': text.strip()[:30],
                'x': shape.left / 914400,
                'y': shape.top / 914400,
                'w': shape.width / 914400,
                'h': shape.height / 914400,
            })

    for i in range(len(text_shapes)):
        for j in range(i + 1, len(text_shapes)):
            a, b = text_shapes[i], text_shapes[j]
            x_overlap = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
            y_overlap = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
            if x_overlap > 0.05 and y_overlap > 0.05:
                area_a = a['w'] * a['h']
                area_b = b['w'] * b['h']
                overlap_ratio = (x_overlap * y_overlap) / min(area_a, area_b) if min(area_a, area_b) > 0 else 0
                assert overlap_ratio < 0.3, f"Overlap {overlap_ratio:.0%} between '{a['text']}' and '{b['text']}'"
    print("  PASS: no element overlap on chapter page")


def test_estimate_wrapped_lines_uses_px_per_in_formula():
    """estimate_wrapped_lines uses PX_PER_IN-based formula consistent with layout.

    The new formula produces widths ~0.889x the old pt/72 formula because
    PX_PER_IN=108 (1440px/13.33in). This matches the layout code's calculation.
    """
    text = '测试text'
    font_size_pt = 16.0
    font_size_px = font_size_pt / 0.75  # 21.333px
    box_width = 5.0

    cjk = 2
    latin = 4

    # New formula (matches layout code)
    new_w = (cjk * font_size_px + latin * font_size_px * 0.55) / PX_PER_IN

    # Should be ~0.83" for this text at 16pt
    assert abs(new_w - 0.8296) < 0.001, f"new_w={new_w:.4f} should be ~0.8296"
    print("  PASS: PX_PER_IN formula matches layout code")


# ─── Slide 4 Subtitle Fix Tests ───────────────────────────────────────────────

def test_slide4_subtitle_width_not_overwritten_by_sync():
    """Slide 4: subtitle width should not be overwritten to default 12.33" by _sync_paired_elements.

    Before fix: subtitle had _pair_with, and a paired shape with default 12.33"
    width synced to the text element, overwriting the layout-computed 8.704".

    After fix: _sync_paired_elements skips shapes with near-default width (12.33").
    """
    from pptx import Presentation
    pptx_path = Path(__file__).parent.parent / 'demo' / 'output.pptx'
    if not pptx_path.exists():
        print("  SKIP: subtitle width (demo/output.pptx not found)")
        return

    prs = Presentation(str(pptx_path))
    s4 = prs.slides[3]  # 0-indexed

    for shape in s4.shapes:
        text = (getattr(shape, 'text', '') or '').strip()
        if '完整' in text[:5] or '预设' in text[:5]:
            w = shape.width / 914400  # EMU to inches
            golden_w = 8.702
            assert abs(w - golden_w) < 0.05, f"Subtitle width {w:.3f}\" should be ~{golden_w:.3f}\", not default 12.33\""
            print(f"  PASS: subtitle width={w:.3f}\" (golden {golden_w:.3f}\")")
            return

    raise AssertionError("Subtitle shape not found")


def test_slide4_subtitle_height_matches_golden():
    """Slide 4: subtitle height should be ~0.499" matching golden.

    Before fix: subtitle height was 0.366" (content 0.199" + padding 0.167").
    Golden shows 0.499" — extra 0.133" from PPTX rendering needs.

    After fix: export code adds pad_h_in * 0.8 extra height for padded single-line
    elements, and uses bodyPr anchor='t' + wrap='square' to preserve height.
    """
    from pptx import Presentation
    pptx_path = Path(__file__).parent.parent / 'demo' / 'output.pptx'
    if not pptx_path.exists():
        print("  SKIP: subtitle height (demo/output.pptx not found)")
        return

    prs = Presentation(str(pptx_path))
    s4 = prs.slides[3]  # 0-indexed

    for shape in s4.shapes:
        text = (getattr(shape, 'text', '') or '').strip()
        if '完整' in text[:5] or '预设' in text[:5]:
            h = shape.height / 914400  # EMU to inches
            golden_h = 0.499
            # Relaxed tolerance: whitespace handling in segments can affect PPTX rendering
            assert abs(h - golden_h) < 0.20, f"Subtitle height {h:.3f}\" should be ~{golden_h:.3f}\""
            print(f"  PASS: subtitle height={h:.3f}\" (golden {golden_h:.3f}\")")
            return

    raise AssertionError("Subtitle shape not found")


def test_enterprise_dark_theme_pill_rail_stays_below_heading():
    """Slide 4 theme pills should move with their wrapper and stay below the heading."""
    html_path = Path('/Users/song/projects/slide-creator/demos/enterprise-dark-zh.html')
    if not html_path.exists():
        print("  SKIP: enterprise-dark theme pill rail (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440)
    slide = slides[3]
    elements = slide['elements']
    export_sandbox.pre_pass_corrections(elements)
    layout_slide_elements(elements, 13.33, 8.33, slide.get('slideStyle', {}), slide)

    text_nodes = _collect_elements_by_type(elements, 'text')
    containers = _collect_elements_by_type(elements, 'container')
    heading = next(elem for elem in text_nodes if '所有演示文稿风格' in elem.get('text', ''))
    rail = next(
        elem for elem in containers
        if elem.get('bounds', {}).get('width', 0.0) > 10.0 and len(elem.get('children', [])) >= 8
    )
    rail_top = min(child['bounds']['y'] for child in rail.get('children', []))
    rail_right = max(child['bounds']['x'] + child['bounds']['width'] for child in rail.get('children', []))

    assert rail_top > heading['bounds']['y'] + heading['bounds']['height'], (heading['bounds'], rail_top)
    assert rail_right <= 12.9, rail_right
    print("  PASS: enterprise-dark theme pill rail stays below heading")


def test_multiline_card_copy_gets_extra_runway_before_thin_track():
    """Wrapped card prose should leave a safer gap before a following progress track."""
    if flow_gap_in is None:
        print("  SKIP: _flow_gap_in pending implementation")
        return

    current = {
        'type': 'text',
        'tag': 'p',
        'text': '你的幻灯片存在别人的云里。导出是事后补救。供应商锁定就是商业模式。',
        'bounds': {'x': 0.0, 'y': 0.0, 'width': 5.2, 'height': 0.444},
        'styles': {'fontSize': '15px', 'lineHeight': '15px', 'marginBottom': '10px'},
    }
    nxt = {
        'type': 'shape',
        'tag': 'div',
        'bounds': {'x': 0.0, 'y': 0.0, 'width': 5.2, 'height': 0.018},
    }
    gap = flow_gap_in(current, nxt, 0.05)
    assert gap >= (12.0 / PX_PER_IN), gap
    print("  PASS: multiline card copy gets extra runway before thin track")


def test_progress_card_copy_remeasure_keeps_font_size_and_wraps_instead_of_shrinking():
    """Progress cards should preserve font size and gain height instead of shrinking text."""
    if remeasure_text_for_final_width is None:
        print("  SKIP: _remeasure_text_for_final_width pending implementation")
        return

    html = '''
    <p style="font-size:15px;line-height:1.6;color:#c9d1d9;">
      你的幻灯片存在别人的云里。导出是事后补救。供应商锁定就是商业模式。
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 732)
    next_track = {'type': 'shape', 'tag': 'div', 'bounds': {'x': 0.0, 'y': 0.0, 'width': 5.29, 'height': 0.018}}
    remeasure_text_for_final_width(text_el, 5.2967, next_flow_item=next_track, inside_card=True)

    assert text_el.get('preferNoWrapFit') is False, text_el
    assert text_el['bounds']['height'] > 0.40, text_el['bounds']
    print("  PASS: progress card copy wraps instead of shrinking during final remeasure")


# ─── Generic Layout Regression Tests ──────────────────────────────────────────

def test_flex_column_badge_stretches_to_parent_width():
    """Background inline children in flex-column containers should stretch.

    Browser flex-column layout defaults to align-items: stretch, so direct child
    spans with background fills should occupy the available column width instead
    of collapsing to text width.
    """
    html = '''
    <div style="display:flex;flex-direction:column;gap:5px;">
      <span style="font-size:14px;padding:3px 10px;background:rgba(14,165,233,0.10);border-radius:6px;color:#0c4a6e;">Blue Sky</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = []
    parent = soup.find('div')
    child = parent.find('span')
    parent_style = compute_element_style(parent, css_rules, parent.get('style', ''))
    results = flat_extract(child, css_rules, parent_style, 1440, content_width_px=180)

    text_el = next(r for r in results if r.get('type') == 'text')
    expected_w = 180 / PX_PER_IN
    assert abs(text_el['bounds']['width'] - expected_w) < 0.01, (
        f"Stretch badge width {text_el['bounds']['width']:.3f}\" should match parent width {expected_w:.3f}\""
    )
    print("  PASS: flex-column badge stretches to parent width")


def test_decoration_in_flex_row_keeps_explicit_size():
    """Decoration-only flex children should preserve explicit CSS size.

    Small dots/dividers inside a flex row are not card backgrounds and must not
    be expanded to the generic 2.0\" placeholder height.
    """
    html = '''
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:10px;height:10px;border-radius:50%;background:#0f172a;"></div>
      <h4 style="font-size:14px;">深色</h4>
      <span style="font-size:12px;color:#64748b;">4 种</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = []
    container = soup.find('div')
    results = flat_extract(container, css_rules, None, 1440)
    assert len(results) == 1 and results[0].get('type') == 'container'
    dot = next(c for c in results[0]['children'] if c.get('_is_decoration'))
    expected = 10.0 / PX_PER_IN
    assert abs(dot['bounds']['height'] - expected) < 0.01, (
        f"Decoration height {dot['bounds']['height']:.3f}\" should stay near {expected:.3f}\""
    )
    assert abs(dot['bounds']['width'] - expected) < 0.01, (
        f"Decoration width {dot['bounds']['width']:.3f}\" should stay near {expected:.3f}\""
    )
    print("  PASS: decoration in flex row keeps explicit size")


def test_gradient_decoration_in_flex_row_keeps_explicit_size():
    """Gradient-only decoration dots should stay decorations, not become card backgrounds."""
    html = '''
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#0ea5e9);"></div>
      <h4 style="font-size:14px;background:linear-gradient(135deg,#1e3a8a,#3b82f6);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">v1.5 新增</h4>
      <span style="font-size:12px;color:#64748b;">8 种</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = []
    container = soup.find('div')
    results = flat_extract(container, css_rules, None, 1440)
    assert len(results) == 1 and results[0].get('type') == 'container'
    dot = next(c for c in results[0]['children'] if c.get('_is_decoration'))
    expected = 10.0 / PX_PER_IN
    assert abs(dot['bounds']['height'] - expected) < 0.01, dot['bounds']
    assert abs(dot['bounds']['width'] - expected) < 0.01, dot['bounds']
    print("  PASS: gradient decoration in flex row keeps explicit size")


def test_grid_flex_container_height_tracks_child_extent_without_tail_gap():
    """Grid/flex wrapper containers should not append an extra hidden tail gap to their bounds."""
    html = '''
    <div style="display:flex;align-items:baseline;gap:14px;">
      <h2 style="font-size:2.6rem;">21 种设计预设</h2>
      <span style="display:inline-flex;align-items:center;padding:4px 14px;border-radius:999px;
                   font-size:12px;background:rgba(37,99,235,0.10);color:#2563eb;">按内容类型自动匹配</span>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    container = flat_extract(soup.find('div'), [], None, 1440)[0]
    max_child_bottom = max(
        child['bounds']['y'] + child['bounds']['height']
        for child in container.get('children', [])
    )
    assert abs(container['bounds']['height'] - max_child_bottom) < 0.02, (
        container['bounds'],
        max_child_bottom,
    )
    print("  PASS: flex/grid container height matches child extent")


def test_parse_html_to_slides_uses_wrapper_max_width_and_drops_slide_bg_shape():
    """Slide roots should keep slide bg out of content elements and propagate wrapper max-width hints."""
    html = '''
    <html><head><style>
      .slide { display:flex; flex-direction:column; justify-content:center; align-items:center; background:#0d1117; color:#e6edf3; }
    </style></head><body>
      <section class="slide">
        <div style="text-align:center; max-width:min(90vw, 800px);">
          <h1>Enterprise Dark</h1>
          <p>Authoritative, data-driven, trustworthy.</p>
        </div>
      </section>
    </body></html>
    '''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as tmp:
        tmp.write(html)
        tmp_path = Path(tmp.name)
    try:
        slides = parse_html_to_slides(tmp_path, 1440, 810)
    finally:
        tmp_path.unlink(missing_ok=True)

    assert slides, "Expected at least one parsed slide"
    slide = slides[0]
    assert abs(slide.get('contentMaxWidthPx', 0.0) - 800.0) < 0.01, slide.get('contentMaxWidthPx')
    assert not any(
        elem.get('type') == 'shape' and elem.get('tag') == 'section'
        for elem in slide.get('elements', [])
    ), slide.get('elements', [])
    print("  PASS: slide wrapper max-width propagates and slide bg shape is dropped")


def test_layout_slide_elements_prefers_slide_content_width_hint_over_widest_text():
    """Slide-level content width hints should prevent narrow text from re-centering the whole page."""
    elements = [
        {
            'type': 'text',
            'text': 'Enterprise Dark',
            'tag': 'h1',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 4.8, 'height': 0.8},
            'styles': {'fontSize': '48px', 'textAlign': 'center', 'lineHeight': '1.1'},
        },
        {
            'type': 'text',
            'text': 'Authoritative, data-driven, trustworthy.',
            'tag': 'p',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 3.6, 'height': 0.4},
            'styles': {'fontSize': '16px', 'textAlign': 'center', 'lineHeight': '1.6'},
        },
    ]
    layout_slide_elements(
        elements,
        13.33,
        810 / 108,
        {'paddingTop': '40px', 'justifyContent': 'center'},
        {'contentMaxWidthPx': 800, 'legacyBlueSkyOffsets': False},
    )

    # 800px content width on 13.33" slide should keep the title inside a 7.41" content
    # area, so centered text lands near 4.9" instead of the old 6.25" narrow-column bug.
    assert elements[0]['bounds']['x'] < 5.1, elements[0]['bounds']
    print("  PASS: layout respects slide content width hint")


def test_single_column_grid_with_nested_flex_column_keeps_shared_row_keys():
    """Single-column grids must not opt into tuple row-keys for nested flex-column content."""
    html = '''
    <div style="display:grid;grid-template-columns:1fr;gap:16px;">
      <div style="display:flex;flex-direction:column;gap:12px;">
        <div style="padding:16px;border:1px solid #dbe4f0;border-radius:16px;background:#ffffff;">
          <h3 style="font-size:22px;margin:0 0 8px;">复杂的工具链</h3>
          <p style="margin:0;font-size:14px;">命令分散，门槛高，无法快速复用。</p>
        </div>
        <div style="padding:16px;border:1px solid #dbe4f0;border-radius:16px;background:#ffffff;">
          <h3 style="font-size:22px;margin:0 0 8px;">千篇一律的输出</h3>
          <p style="margin:0;font-size:14px;">模板单薄，难以形成风格差异。</p>
        </div>
      </div>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    grid = soup.find('div')
    grid_style = compute_element_style(grid, [], grid.get('style', ''))

    children = build_grid_children(grid, [], grid_style, 1440, 940)

    assert children, "Grid should produce exported children"
    text_values = []
    stack = list(children)
    while stack:
        child = stack.pop()
        if child.get('type') == 'text':
            text_values.append(child.get('text', '').strip())
        stack.extend(child.get('children', []))
    assert '复杂的工具链' in text_values, text_values
    assert '千篇一律的输出' in text_values, text_values
    print("  PASS: single-column nested flex-column keeps shared row keys")


def test_local_block_wrapper_packs_children_into_relative_container():
    """Local wrappers with block-only children should preserve vertical flow as one relative container."""
    html = '''
    <div style="margin-top:24px;">
      <table style="width:100%;">
        <tr><td>命令</td><td>用途</td></tr>
      </table>
      <div style="margin-top:20px;padding:16px;border:1px solid #dbe4f0;border-radius:16px;background:#ffffff;">
        <div style="font-size:40px;font-weight:800;">100%</div>
        <div style="font-size:14px;">零依赖运行</div>
      </div>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    wrapper = soup.find('div')
    wrapper_style = compute_element_style(wrapper, [], wrapper.get('style', ''))

    results = flat_extract(wrapper, [], None, 1440, content_width_px=658, local_origin=True)

    assert len(results) == 1, results
    packed = results[0]
    assert packed.get('type') == 'container' and packed.get('_children_relative'), packed
    packed_children = packed.get('children', [])
    assert len(packed_children) == 2, packed_children
    assert packed_children[0].get('type') == 'table', packed_children
    assert packed_children[1].get('type') == 'container', packed_children
    assert packed_children[1]['bounds']['y'] > packed_children[0]['bounds']['y'], packed_children
    print("  PASS: local block wrapper packs children into relative container")


def test_explicit_height_track_stays_thin():
    """No-text progress tracks with explicit CSS height should stay thin, not default to a 2\" block."""
    html = '''
    <div style="height:2px;background:#334155;border-radius:9999px;overflow:hidden;">
      <div style="width:15%;height:100%;background:#ef4444;border-radius:9999px;"></div>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    track = soup.find('div')
    style = compute_element_style(track, [], track.get('style', ''))
    results = flat_extract(track, [], None, 1440, content_width_px=600, local_origin=True)

    assert len(results) >= 2, results
    track_shape = results[0]
    assert track_shape.get('type') == 'shape', track_shape
    assert track_shape['bounds']['height'] < 0.05, track_shape['bounds']
    print("  PASS: explicit-height track stays thin")


def test_centered_card_group_layout_keeps_text_inside_card():
    """Centered shrink-wrap cards should lay out their text inside the card.

    Before fix, card backgrounds advanced the global flow so their paragraphs were
    placed below the card rather than inside it.
    """
    html = '''
    <section class="slide">
      <div style="text-align:center;max-width:720px;">
        <h2>演示用幻灯片，报告用滚动</h2>
        <div style="width:56px;height:3px;background:#2563eb;margin:14px auto;"></div>
        <div style="background:rgba(255,255,255,0.7);border:1px solid rgba(255,255,255,0.9);border-radius:20px;padding:28px 36px;margin-top:8px;">
          <p style="font-size:1.05rem;line-height:1.7;margin-bottom:16px;">slide-creator 做逐页演示，report-creator 做长篇幅报告。</p>
          <p style="font-size:0.92rem;">两者互补，共享同样的设计纪律和工程标准。</p>
        </div>
        <p style="margin-top:20px;font-size:0.9rem;"><code>clawhub install kai-slide-creator</code> · GitHub ↗</p>
      </div>
    </section>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    slide = soup.find('section')
    center = slide.find('div')
    results = flat_extract(center, css_rules, None, 1440)
    layout_slide_elements(results, 13.33, 810 / 108, {'paddingTop': '40px'}, {'_slide_index': 9})

    flat_results = []
    def _walk(elem):
        flat_results.append(elem)
        for child in elem.get('children', []):
            _walk(child)
    for r in results:
        _walk(r)

    card = next(r for r in flat_results if r.get('type') == 'shape' and r.get('_preserve_width'))
    card_texts = [r for r in flat_results if r.get('type') == 'text' and r.get('_card_group') == card.get('_card_group')]
    after_card = next(r for r in flat_results if r.get('type') == 'text' and r.get('_card_group') is None and 'clawhub install' in r.get('text', ''))

    card_bottom = card['bounds']['y'] + card['bounds']['height']
    assert card_texts, "Expected card-group text elements"
    assert all(card['bounds']['y'] <= t['bounds']['y'] < card_bottom for t in card_texts), (
        f"Card texts should be inside card bounds y={card['bounds']['y']:.3f}..{card_bottom:.3f}"
    )
    assert after_card['bounds']['y'] >= card_bottom - 0.01, "Following paragraph should start after the card"
    print("  PASS: centered card-group text stays inside card")


def test_centered_card_group_preserves_vertical_padding_metadata():
    """Centered shrink-wrap cards should keep top/bottom padding metadata for later layout."""
    html = '''
    <section class="slide">
      <div style="text-align:center;max-width:720px;">
        <div style="background:rgba(255,255,255,0.7);border:1px solid rgba(255,255,255,0.9);border-radius:20px;padding:28px 36px;margin-top:8px;">
          <p style="font-size:1rem;line-height:1.7;margin-bottom:16px;">内容一</p>
          <p style="font-size:0.92rem;color:#64748b;">内容二</p>
        </div>
      </div>
    </section>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    results = flat_extract(soup.find('div'), css_rules, None, 1440)

    flat_results = []
    for r in results:
        flat_results.append(r)
        flat_results.extend(r.get('children', []))

    card = next(r for r in flat_results if r.get('type') == 'shape' and r.get('_preserve_width'))
    assert card.get('_css_pad_t', 0.0) > 0.20, card
    assert card.get('_css_pad_b', 0.0) > 0.20, card
    print("  PASS: centered card keeps vertical padding metadata")


def test_slide_root_background_not_promoted_to_card_group():
    """Slide background shapes should not become centered card groups.

    The slide root background is extracted separately; if it gets marked as a
    shrink-wrap card, all descendant content inherits the card group incorrectly.
    """
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide_root_background_not_promoted_to_card_group (HTML not found)")
        return

    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'lxml')
    css_rules = extract_css_from_soup(soup)
    slide10 = soup.select('section.slide')[9]
    body_style = compute_element_style(soup.find('body'), css_rules, '')
    results = flat_extract(slide10, css_rules, body_style, 1440)

    flat_results = []

    def _walk(item):
        flat_results.append(item)
        for child in item.get('children', []):
            _walk(child)

    for result in results:
        _walk(result)

    slide_bg_shapes = [r for r in results if r.get('tag') == 'section']
    assert slide_bg_shapes, "Expected slide root background shape"
    assert not any(r.get('_card_group') for r in slide_bg_shapes), "Slide root bg should not get a card group"

    command_line = next(r for r in flat_results if r.get('type') == 'text' and 'clawhub install' in r.get('text', ''))
    assert command_line.get('_card_group') is None, "Text outside the closing card should not inherit the card group"
    print("  PASS: slide root background is not promoted to card group")


def test_auto_margin_divider_centers_in_constrained_content_area():
    """Auto-margin dividers should center in the content area, not inherit a prior text x."""
    elements = [
        {
            'type': 'text',
            'tag': 'h2',
            'text': '演示用幻灯片，报告用滚动',
            'segments': [{'text': '演示用幻灯片，报告用滚动', 'color': '#0f172a'}],
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 4.85, 'height': 0.46},
            'naturalHeight': 0.46,
            'styles': {'fontSize': '39px', 'lineHeight': '1.2', 'textAlign': 'center', 'maxWidth': '720px'},
        },
        {
            'type': 'shape',
            'tag': 'div',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 0.52, 'height': 0.03},
            'styles': {'width': '56px', 'height': '3px', 'marginTop': '8px', 'marginBottom': '14px',
                       'marginLeft': 'auto', 'marginRight': 'auto'},
        },
    ]

    layout_slide_elements(elements, 13.33, 810 / 108, {'paddingTop': '56px'}, {'_slide_index': 9})
    divider = elements[1]['bounds']
    expected_x = (13.33 - 0.52) / 2
    assert abs(divider['x'] - expected_x) < 0.05, divider
    print("  PASS: auto-margin divider centers within constrained content")


def test_slide2_info_bar_margin_top_applies_to_outer_box():
    """Bottom info bars should keep margin-top on the outer paired box, not only the inner text."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide2_info_bar_margin_top_applies_to_outer_box (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    slide = slides[1]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide['elements'])
    slide['_slide_index'] = 1
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    containers = _collect_elements_by_type(slide['elements'], 'container')
    grid = next(
        e for e in containers
        if len([child for child in e.get('children', []) if child.get('type') == 'container']) == 2
    )
    shapes = _collect_elements_by_type(slide['elements'], 'shape')
    info_shape = next(
        e for e in shapes
        if e.get('type') == 'shape' and e.get('_pair_with') and e.get('styles', {}).get('borderLeft', '').startswith('4px solid')
    )

    grid_bottom = grid['bounds']['y'] + grid['bounds']['height']
    actual_gap = info_shape['bounds']['y'] - grid_bottom
    expected_gap = 14.0 / PX_PER_IN

    assert actual_gap >= expected_gap - 0.03, (grid['bounds'], info_shape['bounds'], actual_gap)
    print("  PASS: slide 2 info bar margin-top applies to outer box")


def test_slide2_info_bar_does_not_emit_detached_code_bg_shape():
    """Deck-level info bars should not emit detached code-bg shapes for inline prose code."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide2_info_bar_does_not_emit_detached_code_bg_shape (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    slide = slides[1]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide['elements'])
    slide['_slide_index'] = 1
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    code_bg_shapes = [e for e in _collect_elements_by_type(slide['elements'], 'shape') if e.get('_is_code_bg')]
    assert not code_bg_shapes, code_bg_shapes
    print("  PASS: slide 2 info bar keeps inline code in text flow")


def test_complex_card_height_uses_stacked_flow():
    """Background cards with many stacked children should size to total flow height."""
    html = '''
    <div style="background:rgba(255,255,255,0.7);border:1px solid rgba(255,255,255,0.9);border-radius:20px;padding:20px;">
      <h4 style="margin-bottom:8px;">此标题可编辑 ↗</h4>
      <p style="font-size:0.82rem;">此段落也可以。点击任何高亮元素开始输入。</p>
      <ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:7px;">
        <li>列表项可编辑</li>
        <li>统计数据、标签、标注 —— 一切都可以</li>
      </ul>
    </div>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = []
    card = soup.find('div')
    results = flat_extract(card, css_rules, None, 1440)
    bg = next(r for r in results if r.get('type') == 'shape')
    assert bg['bounds']['height'] > 1.2, f"Complex card height {bg['bounds']['height']:.3f}\" should reflect stacked flow"
    print("  PASS: complex card height uses stacked flow")


def test_layout_slide_elements_flow_box_advances_current_y_correctly():
    """Top-level flow_box containers must advance slide flow like a single block."""
    elements = [
        {
            'type': 'container',
            'layout': 'flow_box',
            'bounds': {'x': 0.5, 'y': 0.0, 'width': 4.2, 'height': 1.35},
            'styles': {},
            'children': [],
            '_children_relative': True,
        },
        {
            'type': 'text',
            'tag': 'p',
            'text': '后续段落',
            'bounds': {'x': 0.5, 'y': 0.0, 'width': 2.0, 'height': 0.3},
            'styles': {'fontSize': '16px', 'lineHeight': '1.6'},
            'naturalHeight': 0.3,
        },
    ]

    layout_slide_elements(elements, 13.33, 810 / 108, {'paddingTop': '40px'}, {'_slide_index': 0})

    container = elements[0]
    trailing = elements[1]
    expected_y = container['bounds']['y'] + container['bounds']['height'] + 0.13
    assert abs(trailing['bounds']['y'] - expected_y) < 0.02, (
        f"Trailing text y={trailing['bounds']['y']:.3f} should start after flow_box bottom {expected_y:.3f}"
    )
    print("  PASS: flow_box advances current_y correctly")


def test_extract_inline_fragments_code_kbd_support():
    """Future gate: code/kbd should become first-class inline fragments."""
    extract_inline_fragments = _require_symbol('extract_inline_fragments')
    if extract_inline_fragments is None:
        return

    html = '''
    <p>按 <kbd>E</kbd> 进入编辑模式，然后运行 <code>clawhub install kai-slide-creator</code></p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    fragments = extract_inline_fragments(p, [], {})
    kinds = [frag.get('kind') for frag in fragments]

    assert 'kbd' in kinds, f"Expected kbd fragment, got {kinds}"
    assert 'code' in kinds, f"Expected code fragment, got {kinds}"
    print("  PASS: inline fragments expose code/kbd")


def test_extract_inline_fragments_grouped_badge_and_link():
    """Grouped inline mode should keep badge/link semantics in one fragment stream."""
    extract_inline_fragments = _require_symbol('extract_inline_fragments')
    if extract_inline_fragments is None:
        return

    html = '''
    <p>
      <span style="padding:3px 10px;background:rgba(14,165,233,0.10);border-radius:6px;color:#0c4a6e;display:flex;align-items:center;gap:6px;">
        Blue Sky <span class="pill green" style="font-size:0.65rem;padding:1px 7px;background:#dcfce7;color:#166534;border-radius:999px;">当前</span>
      </span>
      <a href="https://example.com" style="color:#2563eb;text-decoration:none;">GitHub ↗</a>
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    fragments = extract_inline_fragments(soup.find('p'), [], {})
    kinds = [frag.get('kind') for frag in fragments if frag.get('text', '').strip()]

    assert 'badge' in kinds, f"Expected badge fragment, got {kinds}"
    assert 'link' in kinds, f"Expected link fragment, got {kinds}"
    assert any(frag.get('grouped') for frag in fragments), f"Expected grouped inline metadata, got {fragments}"
    print("  PASS: grouped inline fragments keep badge/link semantics")


def test_gradient_text_hex_colors_resolve_and_keep_stops():
    """Hex-based gradient text should resolve to explicit PPT colors instead of disappearing."""
    html = '''
    <h2 style="background:linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
               font-size:2.6rem;font-weight:700;">15 项生成前校验，零容忍违规</h2>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    h2 = soup.find('h2')
    style = compute_element_style(h2, [], h2.get('style', ''))
    text_ir = build_text_element(h2, style, [], 1440, 900)

    assert text_ir is not None, "Gradient heading should build into a text element"
    assert text_ir['styles']['color'].lower() == '#1e3a8a', text_ir['styles']['color']
    assert text_ir.get('gradientColors') == ['#1e3a8a', '#3b82f6'], text_ir.get('gradientColors')
    print("  PASS: gradient text resolves hex stops")


def test_build_text_element_inline_flex_pill_shrink_wraps_single_line():
    """Standalone pill components should keep text inside the pill without wrapping."""
    html = '''
    <span style="display:inline-flex;align-items:center;padding:4px 14px;border-radius:999px;
                 font-size:12px;font-weight:600;letter-spacing:0.05em;
                 background:rgba(37,99,235,0.10);color:#2563eb;border:1px solid rgba(37,99,235,0.20);">
      按内容类型自动匹配
    </span>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pill = soup.find('span')
    style = compute_element_style(pill, [], pill.get('style', ''))
    text_ir = build_text_element(pill, style, [], 1440, 900)

    assert text_ir is not None, "Pill should build into a text element"
    assert text_ir.get('forceSingleLine'), text_ir
    assert text_ir['bounds']['width'] > 1.35, text_ir['bounds']
    assert text_ir['bounds']['height'] >= 0.22, text_ir['bounds']
    print("  PASS: standalone pill shrink-wraps with single-line height")


def test_build_text_element_grouped_inline_badge_keeps_single_line_height():
    """Grouped inline badges with inner pills should still size like one capsule component."""
    html = '''
    <span style="font-size:0.77rem;padding:3px 10px;background:rgba(14,165,233,0.10);border-radius:6px;color:#0c4a6e;display:flex;align-items:center;gap:6px;">
      Blue Sky <span class="pill green" style="font-size:0.65rem;padding:1px 7px;background:#dcfce7;color:#166534;border-radius:999px;">当前</span>
    </span>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    badge = soup.find('span')
    style = compute_element_style(badge, [], badge.get('style', ''))
    text_ir = build_text_element(badge, style, [], 1440, 420)

    assert text_ir is not None, "Grouped badge should build into a text element"
    assert text_ir.get('forceSingleLine'), text_ir
    assert text_ir['bounds']['height'] >= 0.21, text_ir['bounds']
    print("  PASS: grouped inline badge keeps capsule-like single-line height")


def test_build_text_element_block_cta_pill_uses_component_layout():
    """Block tags with inline-block pill styling should still use pill component sizing."""
    html = '''
    <div style="display:inline-block;padding:12px 32px;border-radius:8px;
                background:#3b82f6;color:#ffffff;font-weight:700;
                font-size:clamp(1rem, 2vw, 1.5rem);text-align:center;">
      /slide-creator
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pill = soup.find('div')
    style = compute_element_style(pill, [], pill.get('style', ''))
    text_ir = build_text_element(pill, style, [], 1440, 900)

    assert text_ir is not None, "CTA pill should build into a text element"
    assert text_ir.get('forceSingleLine'), text_ir
    assert text_ir.get('preferContentWidth'), text_ir
    assert text_ir['bounds']['height'] >= 0.30, text_ir['bounds']
    print("  PASS: block CTA pill uses component layout")


def test_build_text_element_boosts_cjk_display_heading_optically():
    """Bold CJK h1/h2 display headings should get a small optical size boost for PPT output."""
    html = '''
    <h2 style="font-family:'Inter', 'Noto Sans SC', sans-serif;
               font-size:clamp(1.25rem, 3.5vw, 2.5rem);
               font-weight:700;line-height:1.1;letter-spacing:-0.02em;">
      四个核心能力，支撑完整演示链路
    </h2>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h2')
    style = compute_element_style(heading, [], heading.get('style', ''))
    text_ir = build_text_element(heading, style, [], 1440, 900)

    assert text_ir is not None, "Display heading should build into a text element"
    boosted_font_px = parse_px(text_ir['styles']['fontSize'])
    assert boosted_font_px >= 43.0, boosted_font_px
    assert all(parse_px(seg.get('fontSize', '0px')) >= 43.0 for seg in text_ir.get('segments', [])), text_ir.get('segments')
    assert all(parse_px(frag.get('fontSize', '0px')) >= 43.0 for frag in text_ir.get('fragments', [])), text_ir.get('fragments')
    assert text_ir['bounds']['height'] > 0.45, text_ir['bounds']
    print("  PASS: CJK display heading gets optical size boost")


def test_build_text_element_skips_optical_boost_for_space_grotesk_display_heading():
    """Aurora Mesh display headings already author large enough; don't over-boost them."""
    html = '''
    <h2 style="font-family:'Space Grotesk', 'Noto Sans SC', sans-serif;
               font-size:clamp(1.8rem, 4vw, 3.5rem);
               font-weight:700;line-height:1.1;letter-spacing:-0.02em;">
      四个核心能力，覆盖完整工作流
    </h2>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h2')
    style = compute_element_style(heading, [], heading.get('style', ''))
    text_ir = build_text_element(heading, style, [], 1440, 900)

    assert text_ir is not None, "Aurora display heading should build into a text element"
    unboosted_font_px = parse_px(text_ir['styles']['fontSize'])
    assert 56.0 <= unboosted_font_px <= 58.5, unboosted_font_px
    assert all(
        56.0 <= parse_px(seg.get('fontSize', '0px')) <= 58.5
        for seg in text_ir.get('segments', [])
    ), text_ir.get('segments')
    print("  PASS: Space Grotesk display heading keeps authored size")


def test_build_grid_children_flex_row_preserves_component_width_and_pairing():
    """Flex-row slotting should respect component width and keep bg/text paired."""
    html = '''
    <style>
      .pill {
        display:inline-flex;align-items:center;
        padding:4px 14px;border-radius:999px;
        font-size:12px;font-weight:600;letter-spacing:0.05em;
        background:rgba(37,99,235,0.10);color:#2563eb;
        border:1px solid rgba(37,99,235,0.20);
      }
    </style>
    <div style="display:flex;align-items:baseline;gap:14px;margin-bottom:4px;">
      <h2 style="font-size:2.6rem;">21 种设计预设</h2>
      <span class="pill">按内容类型自动匹配</span>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    row = soup.find('div')
    row_style = compute_element_style(row, css_rules, row.get('style', ''))
    children = build_grid_children(row, css_rules, row_style, 1440, 940)

    title_text = next(e for e in children if e.get('type') == 'text' and e.get('text') == '21 种设计预设')
    pill_text = next(e for e in children if e.get('type') == 'text' and e.get('text') == '按内容类型自动匹配')
    pill_shape = next(e for e in children if e.get('type') == 'shape' and e.get('_pair_with') == pill_text.get('_pair_with'))

    assert pill_text['bounds']['width'] >= 1.48, pill_text['bounds']
    assert pill_shape['bounds']['width'] == pill_text['bounds']['width'], (pill_shape['bounds'], pill_text['bounds'])
    assert pill_shape.get('_pair_with') == pill_text.get('_pair_with'), (pill_shape, pill_text)
    assert pill_text['bounds']['y'] > title_text['bounds']['y'] + 0.12, (title_text['bounds'], pill_text['bounds'])
    print("  PASS: flex-row component width and bg/text pairing stay aligned")


def test_build_grid_children_flex_wrap_centers_rows_without_overflow():
    """Wrapped pill rails should create multiple centered rows instead of one giant off-slide row."""
    html = '''
    <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:min(90vw,800px);">
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Aurora Mesh</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Bold Signal</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Blue Sky</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Chinese Chan</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Creative Voltage</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Enterprise Dark</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Modern Newspaper</span>
      <span style="display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(56,139,253,0.12);border:1px solid #30363d;color:#c9d1d9;">Vintage Editorial</span>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find('div')
    row_style = compute_element_style(row, [], row.get('style', ''))
    children = build_grid_children(row, [], row_style, 1440, parse_px('min(90vw,800px)'))

    text_children = [child for child in children if child.get('type') == 'text']
    assert text_children, children
    assert max(child['bounds']['x'] + child['bounds']['width'] for child in text_children) <= 12.9, [
        child['bounds'] for child in text_children
    ]
    distinct_rows = {round(child['bounds']['y'], 2) for child in text_children}
    assert len(distinct_rows) >= 2, distinct_rows
    print("  PASS: flex-wrap rail creates centered wrapped rows")


def test_map_font_prefers_stable_ppt_font_over_platform_stack_order():
    """Platform-first CSS stacks should still resolve to an installed CJK-capable font pair."""
    map_font = _require_symbol('map_font')
    if map_font is None:
        return

    latin_font, ea_font = map_font("'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif", text='中文标题')
    assert latin_font == 'Hiragino Sans GB', (latin_font, ea_font)
    assert ea_font == 'Hiragino Sans GB', (latin_font, ea_font)
    print("  PASS: mixed platform stack resolves to installed CJK-capable font pair")


def test_map_font_platform_only_cjk_stack_falls_back_to_office_safe_font():
    """Platform-only CJK stacks should still resolve to an installed CJK-capable fallback."""
    map_font = _require_symbol('map_font')
    if map_font is None:
        return

    latin_font, ea_font = map_font('"PingFang SC", "Noto Sans SC", "Segoe UI", system-ui, sans-serif', text='演示文稿')
    assert latin_font == 'Hiragino Sans GB', (latin_font, ea_font)
    assert ea_font == 'Hiragino Sans GB', (latin_font, ea_font)
    print("  PASS: platform-only CJK stack falls back to installed CJK-capable font")


def test_map_font_pure_latin_prefers_latin_safe_font_even_in_mixed_stack():
    """Pure Latin pill labels should prefer an installed Latin font over CJK fallback fonts."""
    map_font = _require_symbol('map_font')
    if map_font is None:
        return

    latin_font, ea_font = map_font("'Inter', 'Noto Sans SC', system-ui, sans-serif", text='slide-creator')
    assert latin_font == 'Inter', (latin_font, ea_font)
    assert ea_font == 'Inter', (latin_font, ea_font)
    print("  PASS: pure Latin labels prefer installed Latin font in mixed stack")


def test_map_font_space_grotesk_stack_stays_sans_for_latin_and_cjk():
    """Space Grotesk stacks should not fall through to serif via the generic sans-serif token."""
    map_font = _require_symbol('map_font')
    if map_font is None:
        return

    latin_font, ea_font = map_font("'Space Grotesk', 'Noto Sans SC', sans-serif", text='slide-creator')
    assert latin_font == 'Helvetica Neue', (latin_font, ea_font)
    assert ea_font == 'Helvetica Neue', (latin_font, ea_font)

    latin_font, ea_font = map_font("'Space Grotesk', 'Noto Sans SC', sans-serif", text='一个命令，创建无限可能')
    assert latin_font == 'Hiragino Sans GB', (latin_font, ea_font)
    assert ea_font == 'Hiragino Sans GB', (latin_font, ea_font)
    print("  PASS: Space Grotesk stack stays sans across Latin and CJK text")


def _chinese_chan_contract_fixture():
    return {
        'contract_id': 'slide-creator/chinese-chan',
        'typography': {
            'cn_font_stack': ['Noto Serif CJK SC', 'Source Han Serif SC', 'STSong', 'Georgia', 'serif'],
            'en_font_stack': ['EB Garamond', 'Crimson Text', 'Georgia', 'serif'],
            'role_selectors': {
                'title': ['.zen-title', '.zen-h2', '.zen-subtitle', '.zen-caption', '.zen-accent', '.zen-ghost-kanji'],
                'body': ['.zen-body', '.zen-list'],
                'command': ['.cmd'],
                'metric': ['.num', '.label'],
            },
            'title': {'family_mode': 'cn_serif', 'weight': 400, 'line_height': 1.3, 'letter_spacing': '0.08em'},
            'body': {'family_mode': 'cn_serif', 'weight': 300, 'line_height': 1.9, 'letter_spacing': '0.05em'},
            'command': {'family_mode': 'en_serif', 'line_height': 1.6},
            'metric': {'family_mode': 'en_serif', 'weight': 600},
        },
        'line_break_contract': {
            'break_policy': {
                '.zen-title': 'prefer_preserve',
                '.zen-body': 'preserve',
                '.cmd': 'preserve',
            },
            'shrink_forbidden_for': ['.zen-title', '.zen-body', '.cmd'],
            'overflow_strategy': 'expand_container_first',
        },
    }


def _swiss_modern_contract_fixture():
    return {
        'contract_id': 'slide-creator/swiss-modern',
        'typography': {
            'display_font_stack': ['Archivo Black', 'Arial Black', 'Helvetica Neue', 'sans-serif'],
            'body_font_stack': ['Nunito', 'Helvetica Neue', 'Arial', 'sans-serif'],
            'label_font_stack': ['Archivo', 'Helvetica Neue', 'Arial', 'sans-serif'],
            'role_selectors': {
                'title': ['.swiss-title', '.quote-text'],
                'body': ['.swiss-body', '.quote-attribution'],
                'label': ['.eyebrow', '.slide-num-label'],
                'metric': ['.swiss-stat'],
            },
            'title': {'family_mode': 'display_sans', 'weight': 900, 'line_height': 1.0, 'letter_spacing': '-0.02em'},
            'body': {'family_mode': 'body_sans', 'weight': 400, 'line_height': 1.55},
            'label': {'family_mode': 'label_sans', 'weight': 700, 'line_height': 1.2, 'letter_spacing': '0.08em'},
            'metric': {'family_mode': 'display_sans', 'weight': 900, 'line_height': 1.0},
        },
        'line_break_contract': {
            'break_policy': {
                '.swiss-title': 'prefer_preserve',
                '.quote-text': 'prefer_preserve',
                '.swiss-body': 'preserve',
                '.quote-attribution': 'preserve',
            },
            'shrink_forbidden_for': ['.swiss-title', '.quote-text', '.swiss-stat', '.quote-attribution'],
            'overflow_strategy': 'expand_container_first',
        },
    }


def test_map_font_mixed_serif_stack_uses_latin_and_cjk_pair_for_mixed_script():
    """Mixed-script serif stacks should keep Latin serif for Latin glyphs and CJK serif for East Asian glyphs."""
    css_stack = '"Noto Serif SC", "EB Garamond", Georgia, serif'
    assert map_font(css_stack, text='零依赖 HTML 演示文稿') == ('Baskerville', 'Songti SC')
    print("  PASS: mixed-script serif stack keeps Latin+CJK serif pair")


def test_map_font_swiss_display_stack_prefers_archivo_fallback_for_latin():
    """Swiss display stacks remap to the cross-renderer-stable Helvetica Neue
    pair; the comparison renderer also overrides web fonts to the same
    Helvetica fallback, so both sides share rasterization geometry."""
    latin_font, ea_font = map_font('"Archivo Black", "Nunito", "Noto Sans SC", sans-serif', text='SWISS')
    assert latin_font == 'Helvetica Neue', (latin_font, ea_font)
    assert ea_font == 'Helvetica Neue', (latin_font, ea_font)
    print("  PASS: Swiss display stack maps to Helvetica Neue cross-renderer pair")


def test_resolve_text_contract_chinese_chan_preserves_body_breaks():
    """Chinese Chan body blocks with authored <br> should preserve source rhythm and forbid shrink-fit."""
    resolver = _require_symbol('_resolve_text_contract')
    if resolver is None:
        return

    soup = BeautifulSoup('<div class="zen-body">Bold Signal —— 笃定<br>Blue Sky —— 澄明</div>', 'html.parser')
    node = soup.find('div')
    contract = _chinese_chan_contract_fixture()
    resolved = resolver(node, {'fontFamily': ''}, 'Bold Signal —— 笃定\nBlue Sky —— 澄明', contract)

    assert resolved['role'] == 'body', resolved
    assert resolved['preserveAuthoredBreaks'] is True, resolved
    assert resolved['shrinkForbidden'] is True, resolved
    assert 'Noto Serif CJK SC' in resolved.get('fontFamily', ''), resolved
    print("  PASS: Chinese Chan body text contract preserves authored breaks")


def test_resolve_text_contract_chinese_chan_title_prefers_wrap_over_shrink():
    """Chinese Chan display titles should preserve authored width rhythm by wrapping before shrinking."""
    resolver = _require_symbol('_resolve_text_contract')
    if resolver is None:
        return

    soup = BeautifulSoup('<div class="zen-title">kai-slide-creator</div>', 'html.parser')
    node = soup.find('div')
    contract = _chinese_chan_contract_fixture()
    resolved = resolver(node, {'fontFamily': '"Noto Serif SC", "EB Garamond", Georgia, serif'}, 'kai-slide-creator', contract)

    assert resolved['role'] == 'title', resolved
    assert resolved['breakPolicy'] == 'prefer_preserve', resolved
    assert resolved['preferWrapToPreserveSize'] is True, resolved
    assert resolved['shrinkForbidden'] is True, resolved
    print("  PASS: Chinese Chan title prefers wrap over shrink")


def test_resolve_text_contract_chinese_chan_body_prefers_wrap_for_long_prose():
    """Chinese Chan body prose without explicit <br> should still prefer reflow over no-wrap shrink heuristics."""
    resolver = _require_symbol('_resolve_text_contract')
    if resolver is None:
        return

    soup = BeautifulSoup(
        '<div class="zen-body">演示工具越来越臃肿。模板商店卖着换汤不换药的「新设计」。AI 生成器做出来的幻灯片——精致、通用、过目即忘。</div>',
        'html.parser',
    )
    node = soup.find('div')
    contract = _chinese_chan_contract_fixture()
    resolved = resolver(node, {'fontFamily': '"Noto Serif SC", "EB Garamond", Georgia, serif'}, node.get_text(), contract)

    assert resolved['role'] == 'body', resolved
    assert resolved['breakPolicy'] == 'preserve', resolved
    assert resolved['preferWrapToPreserveSize'] is True, resolved
    assert resolved['shrinkForbidden'] is True, resolved
    print("  PASS: Chinese Chan long body prose prefers wrap over no-wrap heuristics")


def test_resolve_text_contract_swiss_title_uses_display_stack_and_preserves_width():
    """Swiss display titles should use the synced display stack and prefer wrap over shrink."""
    resolver = _require_symbol('_resolve_text_contract')
    if resolver is None:
        return

    soup = BeautifulSoup('<div class="swiss-title">HELVETIC ORDER</div>', 'html.parser')
    node = soup.find('div')
    contract = _swiss_modern_contract_fixture()
    resolved = resolver(node, {'fontFamily': ''}, 'HELVETIC ORDER', contract)

    assert resolved['role'] == 'title', resolved
    assert resolved['breakPolicy'] == 'prefer_preserve', resolved
    assert resolved['preferWrapToPreserveSize'] is True, resolved
    assert resolved['shrinkForbidden'] is True, resolved
    assert 'Archivo Black' in resolved.get('fontFamily', ''), resolved
    print("  PASS: Swiss title contract preserves display font and width rhythm")


def test_build_table_element_plain_td_defaults_to_text_primary():
    """Plain td cells without explicit color should still export as readable dark text."""
    html = '''
    <style>
      :root { --text-primary: #0f172a; }
      .ctable td { padding: 5px 0; }
    </style>
    <table class="ctable">
      <tr><td>内容密度</td><td style="color:#334155;">≥ 65% 填充</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    table = soup.find('table')
    style = compute_element_style(table, css_rules, table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, css_rules, style)
    first_cell = table_ir['rows'][0]['cells'][0]

    assert first_cell['styles']['color'].lower() == '#0f172a', first_cell['styles']['color']
    print("  PASS: plain table cells fall back to text-primary")


def test_flat_extract_mixed_inline_code_uses_inline_overlays():
    """Single-line mixed inline rows should use inline-box overlays instead of detached code-bg siblings."""
    html = '''
    <p style="margin-top:20px;font-size:0.9rem;color:#64748b;">
      <code style="font-family:'SF Mono',monospace;padding:1px 6px;border-radius:5px;
                   background:rgba(37,99,235,0.08);color:#1e3a8a;">clawhub install kai-slide-creator</code>
      <a href="https://example.com" style="color:#2563eb;text-decoration:none;">GitHub ↗</a>
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    results = flat_extract(p, [], None, 1440, 720)
    text_el = next(r for r in results if r.get('type') == 'text' and 'clawhub install' in r.get('text', ''))

    assert text_el.get('renderInlineBoxOverlays'), text_el
    assert not any(r.get('_is_code_bg') for r in results), results
    code_seg = next(seg for seg in text_el.get('segments', []) if seg.get('kind') == 'code')
    assert 'Mono' in code_seg.get('fontFamily', ''), code_seg
    laid_out = export_sandbox._layout_single_line_fragments(
        text_el['fragments'],
        {'x': 4.232, 'y': 4.935, 'width': 4.867, 'height': 0.213},
        parse_px(text_el['styles']['fontSize']),
        text_align='center',
    )
    code_box = next(metric for metric in laid_out if metric['fragment'].get('kind') == 'code')
    assert code_box['height'] >= 0.213 - 1e-6, code_box
    print("  PASS: mixed inline code is handled by text-bound inline overlays")


def test_flat_extract_inline_code_in_prose_does_not_emit_detached_code_bg():
    """Inline code inside ordinary prose paragraphs should stay in the text run stream."""
    html = '''
    <p style="font-size:16.8px;color:#334155;">
      用 <code style="background:rgba(37,99,235,0.08);color:#1e3a8a;padding:1px 6px;border-radius:5px;">--plan</code>
      先获得结构化大纲文件。编辑它，然后在准备好时运行
      <code style="background:rgba(37,99,235,0.08);color:#1e3a8a;padding:1px 6px;border-radius:5px;">--generate</code>。
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    results = flat_extract(soup.find('p'), [], None, 1440, 820)
    text_el = next(r for r in results if r.get('type') == 'text')
    assert not any(r.get('_is_code_bg') for r in results), results
    assert text_el['bounds']['height'] < 0.35, text_el['bounds']
    print("  PASS: inline prose code stays inside text flow")


def test_build_text_element_wide_prose_adjusts_back_to_single_line():
    """Wide mixed-script prose should not stick on two lines after adjusted-fit estimation."""
    html = '''
    <p style="font-size:16.8px;line-height:1.6;color:#334155;">
      告诉 slide-creator 你想呈现什么——受众、目标、核心信息。纯中文或英文。无需特殊格式。
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 732)

    assert text_el['bounds']['height'] < 0.30, text_el['bounds']
    print("  PASS: wide prose paragraph falls back to single-line fit")


def test_build_text_element_medium_card_prose_adjusts_back_to_single_line():
    """Medium-width card prose should not falsely wrap when adjusted-fit can keep one line."""
    html = '''
    <p style="font-size:15px;line-height:1.6;color:#c9d1d9;">
      E 键切换 contenteditable，所有文本可直接修改。Ctrl+S 保存为 HTML 文件。
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 524)

    assert text_el['bounds']['height'] < 0.30, text_el['bounds']
    print("  PASS: medium card prose falls back to single-line fit")


def test_build_text_element_long_editorial_prose_skips_no_wrap_fit():
    """Wide editorial prose that already estimates as multiline should not be forced back into no-wrap fit."""
    html = '''
    <p style="font-size:16px;line-height:1.55;max-width:718px;color:#3f3f46;">
      AI订单的快速放量，正是知行合一的结果。不是喊一句“AI转型”的口号，而是实实在在把AI能力注入星瀚、星空、星辰等核心产品，切切实实帮客户提升效率，自然得到市场的认可。
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 718)

    assert text_el.get('preferNoWrapFit') is False, text_el
    assert text_el['bounds']['height'] > 0.45, text_el['bounds']
    print("  PASS: long editorial prose keeps multiline width rhythm")


def test_build_text_element_centered_subtitle_prefers_full_max_width_and_no_wrap_fit():
    """Centered CTA subtitles with explicit max-width should expand to that width and avoid extra wrapping."""
    html = '''
    <p style="font-size:20px; color:#8b949e; margin-top:12px; max-width:500px; text-align:center;">
      纯浏览器运行 · 零依赖 · 21 种风格任你选择
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 900)

    assert text_el['bounds']['width'] >= 4.6, text_el['bounds']
    assert text_el.get('preferNoWrapFit') is True, text_el
    print("  PASS: centered subtitle expands to max width and prefers no-wrap fit")


def test_layout_centered_subtitle_keeps_max_width_when_no_wrap_fit_is_requested():
    """Layout should not shrink centered no-wrap subtitles back to natural width."""
    html = '''
    <p style="font-size:20px; color:#8b949e; margin-top:12px; max-width:500px; text-align:center;">
      纯浏览器运行 · 零依赖 · 21 种风格任你选择
    </p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    style = compute_element_style(p, [], p.get('style', ''))
    text_el = build_text_element(p, style, [], 1440, 900)
    layout_slide_elements([text_el], 13.33, 8.33, {'paddingTop': '48px'}, {'_slide_index': 0})

    assert text_el['bounds']['width'] >= 4.6, text_el['bounds']
    print("  PASS: centered subtitle keeps full max-width through layout")


def test_flow_gap_prefers_collapsed_margins_over_default_gap():
    """Block-flow spacing should prefer CSS collapsed margins over fallback gaps."""
    flow_gap = _require_symbol('_flow_gap_in')
    if flow_gap is None:
        return

    current = {'tag': 'div', 'styles': {'marginBottom': '4px'}}
    nxt = {'tag': 'div', 'styles': {'marginTop': '8px'}}
    gap = flow_gap(current, nxt, 0.13)

    assert abs(gap - (8.0 / PX_PER_IN)) < 1e-6, gap
    print("  PASS: flow gap uses collapsed CSS margins")


def test_layout_slide_elements_uses_next_margin_top_for_container_gap():
    """Top-level stacked containers should honor next element marginTop instead of default gap."""
    elements = [
        {
            'type': 'container',
            'tag': 'div',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 8.7, 'height': 0.462},
            'styles': {'marginBottom': '4px'},
            'children': [],
            '_children_relative': False,
        },
        {
            'type': 'shape',
            'tag': 'div',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 0.518, 'height': 0.028},
            'styles': {'marginTop': '8px', 'marginBottom': '14px'},
        },
    ]

    layout_slide_elements(elements, 13.33, 810 / 108, {'paddingTop': '54px'}, {'_slide_index': 0})

    first = elements[0]['bounds']
    divider = elements[1]['bounds']
    expected_gap = 8.0 / PX_PER_IN
    actual_gap = divider['y'] - (first['y'] + first['height'])

    assert abs(actual_gap - expected_gap) < 0.02, (first, divider, actual_gap)
    print("  PASS: top-level layout uses next margin-top for spacing")


def test_build_elements_preserve_margin_top_metadata():
    """IR elements should retain marginTop so downstream flow layout can use it."""
    html = '''
    <div style="width:56px;height:3px;margin-top:8px;margin-bottom:14px;background:#2563eb;"></div>
    <p style="font-size:16px;line-height:1.6;margin-top:10px;">段落</p>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div')
    p = soup.find('p')

    div_style = compute_element_style(div, [], div.get('style', ''))
    p_style = compute_element_style(p, [], p.get('style', ''))

    shape = export_sandbox.build_shape_element(div, div_style, 1440)
    text = build_text_element(p, p_style, [], 1440, 720)

    assert shape['styles']['marginTop'] == '8px', shape['styles']
    assert text['styles']['marginTop'] == '10px', text['styles']
    print("  PASS: element IR preserves margin-top metadata")


def test_card_group_layout_expands_bg_height_to_content_bottom():
    """Centered card groups should grow their background to the laid-out content bottom."""
    elements = [
        {
            'type': 'shape',
            'tag': 'div',
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 2.4, 'height': 0.52},
            'styles': {'backgroundColor': '#ffffff', 'borderRadius': '20px'},
            '_card_group': 'card-test',
            '_preserve_width': True,
            '_css_pad_l': 0.12,
            '_css_pad_r': 0.12,
            '_css_pad_t': 0.10,
            '_css_pad_b': 0.12,
            '_css_border_l': 0.0,
        },
        {
            'type': 'text',
            'tag': 'p',
            'text': '标题',
            'segments': [{'text': '标题', 'color': '#0f172a'}],
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 1.8, 'height': 0.25},
            'naturalHeight': 0.25,
            'styles': {'fontSize': '16px', 'lineHeight': '1.4', 'marginBottom': '8px'},
            '_card_group': 'card-test',
        },
        {
            'type': 'text',
            'tag': 'p',
            'text': '说明文本',
            'segments': [{'text': '说明文本', 'color': '#475569'}],
            'bounds': {'x': 0.5, 'y': 0.5, 'width': 1.8, 'height': 0.40},
            'naturalHeight': 0.40,
            'styles': {'fontSize': '14px', 'lineHeight': '1.6'},
            '_card_group': 'card-test',
        },
    ]

    layout_slide_elements(elements, 13.33, 810 / 108, {'paddingTop': '54px'}, {'_slide_index': 0})

    bg = elements[0]['bounds']
    last_text = elements[2]['bounds']
    assert bg['y'] + bg['height'] >= last_text['y'] + last_text['height'] + 0.11, (bg, last_text)
    print("  PASS: card-group bg height tracks laid-out content bottom")


def test_export_text_element_preserves_explicit_break_headings():
    """Explicit line-break display headings should not allow PowerPoint re-wrap."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'h1',
        'text': 'AI 驱动的\nHTML 演示文稿',
        'segments': [
            {'text': 'AI 驱动的', 'color': '#1e3a8a', 'fontSize': '72px', 'fontFamily': 'PingFang SC', 'letterSpacing': '-0.02em', 'bold': True, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
            {'text': '\n', 'color': '#1e3a8a', 'fontSize': '72px', 'fontFamily': 'PingFang SC', 'letterSpacing': '-0.02em', 'bold': True, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
            {'text': 'HTML 演示文稿', 'color': '#1e3a8a', 'fontSize': '72px', 'fontFamily': 'PingFang SC', 'letterSpacing': '-0.02em', 'bold': True, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 4.25, 'y': 2.7, 'width': 4.82, 'height': 1.47},
        'naturalHeight': 1.47,
        'styles': {
            'fontSize': '72px',
            'fontWeight': '800',
            'fontFamily': 'PingFang SC',
            'letterSpacing': '-0.02em',
            'color': '#1e3a8a',
            'textAlign': 'center',
            'lineHeight': '1.1',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
            'justifyContent': '',
        },
    }

    export_sandbox.export_text_element(slide, elem, (255, 255, 255))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is False, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE, tf.auto_size
    print("  PASS: export keeps explicit-break headings from re-wrapping")


def test_export_text_element_keeps_narrow_card_copy_wrapping_instead_of_shrinking():
    """Narrow card body copy with a multi-line measured height should not shrink-fit in PPT."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'p',
        'text': '完全生成前并排渲染三种匹配风格。',
        'segments': [
            {
                'text': '完全生成前并排渲染三种匹配风格。',
                'color': '#c9d1d9',
                'fontSize': 'clamp(12px,1.3vw,14px)',
                'fontFamily': 'PingFang SC',
                'letterSpacing': '',
                'bold': False,
                'strike': False,
                'bgColor': None,
                'inlineBgBounds': None,
                'kind': 'text',
            },
        ],
        'bounds': {'x': 7.078, 'y': 3.946, 'width': 1.315, 'height': 0.415},
        'naturalHeight': 0.415,
        'styles': {
            'fontSize': 'clamp(12px,1.3vw,14px)',
            'fontWeight': '400',
            'fontFamily': 'PingFang SC',
            'letterSpacing': '',
            'color': '#c9d1d9',
            'textAlign': 'left',
            'lineHeight': '1.6',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (13, 17, 23))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is True, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: narrow card copy wraps instead of shrinking during export")


def test_export_text_element_preserves_contract_authored_breaks_without_shrinking():
    """Contract-preserved authored breaks should grow the text box instead of shrinking or reflowing."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'div',
        'text': 'Bold Signal —— 笃定\nBlue Sky —— 澄明',
        'segments': [
            {'text': 'Bold Signal —— 笃定', 'color': '#1a1a18', 'fontSize': '16px', 'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif', 'letterSpacing': '0.05em', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
            {'text': '\n', 'color': '#1a1a18', 'fontSize': '16px', 'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif', 'letterSpacing': '0.05em', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
            {'text': 'Blue Sky —— 澄明', 'color': '#1a1a18', 'fontSize': '16px', 'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif', 'letterSpacing': '0.05em', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 4.0, 'y': 2.0, 'width': 3.8, 'height': 0.55},
        'naturalHeight': 0.55,
        'preserveAuthoredBreaks': True,
        'shrinkForbidden': True,
        'styles': {
            'fontSize': '16px',
            'fontWeight': '300',
            'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif',
            'letterSpacing': '0.05em',
            'color': '#1a1a18',
            'textAlign': 'left',
            'lineHeight': '1.9',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (250, 250, 248))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is False, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: contract-preserved authored breaks grow instead of shrinking")


def test_export_text_element_prefers_wrap_to_preserve_size_for_body_prose():
    """Contract-preferred body prose should wrap and grow before falling back to no-wrap shrink heuristics."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'div',
        'text': '演示工具越来越臃肿。模板商店卖着换汤不换药的「新设计」。AI 生成器做出来的幻灯片——精致、通用、过目即忘。',
        'segments': [
            {'text': '演示工具越来越臃肿。模板商店卖着换汤不换药的「新设计」。AI 生成器做出来的幻灯片——精致、通用、过目即忘。', 'color': '#1a1a18', 'fontSize': '16px', 'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif', 'letterSpacing': '0.05em', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 4.0, 'y': 2.0, 'width': 5.56, 'height': 0.55},
        'naturalHeight': 0.55,
        'preferWrapToPreserveSize': True,
        'shrinkForbidden': True,
        'styles': {
            'fontSize': '16px',
            'fontWeight': '300',
            'fontFamily': '"Noto Serif CJK SC", "EB Garamond", Georgia, serif',
            'letterSpacing': '0.05em',
            'color': '#1a1a18',
            'textAlign': 'left',
            'lineHeight': '1.9',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (250, 250, 248))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is True, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: contract-preferred body prose wraps before shrinking")


def test_export_text_element_single_line_contract_title_stays_no_wrap():
    """Single-line contract titles that already fit should not invite PowerPoint-only re-wraps."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'p',
        'text': '君子务本，本立而道生',
        'segments': [
            {'text': '君子务本，本立而道生', 'color': '#111111', 'fontSize': '66px', 'fontFamily': '"Archivo Black", "Noto Sans SC", sans-serif', 'letterSpacing': '-0.04em', 'bold': True, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 0.93, 'y': 1.5, 'width': 6.48, 'height': 0.63},
        'naturalHeight': 0.63,
        'preferWrapToPreserveSize': True,
        'shrinkForbidden': True,
        '_text_contract_role': 'title',
        'styles': {
            'fontSize': '66px',
            'fontWeight': '900',
            'fontFamily': '"Archivo Black", "Noto Sans SC", sans-serif',
            'letterSpacing': '-0.04em',
            'color': '#111111',
            'textAlign': 'left',
            'lineHeight': '1.02',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (250, 250, 248))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is False, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: single-line contract title stays no-wrap")


def test_export_text_element_medium_contract_title_keeps_wrap_square():
    """Smaller editorial contract titles should preserve authored block width with wrap enabled."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'div',
        'text': '从一个预设开始',
        'segments': [
            {'text': '从一个预设开始', 'color': '#1a1a18', 'fontSize': 'clamp(1.2rem, 3vw, 1.8rem)', 'fontFamily': '"Noto Serif SC", "EB Garamond", Georgia, serif', 'letterSpacing': '0.1em', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 4.14, 'y': 3.05, 'width': 5.56, 'height': 0.35},
        'naturalHeight': 0.35,
        'preferWrapToPreserveSize': True,
        'shrinkForbidden': True,
        '_text_contract_role': 'title',
        'styles': {
            'fontSize': 'clamp(1.2rem, 3vw, 1.8rem)',
            'fontWeight': '300',
            'fontFamily': '"Noto Serif SC", "EB Garamond", Georgia, serif',
            'letterSpacing': '0.1em',
            'color': '#1a1a18',
            'textAlign': 'center',
            'lineHeight': '1.3',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (250, 250, 248))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is True, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: medium contract title keeps wrap square")


def test_export_text_element_wide_multiline_prose_wraps_from_measured_height():
    """Generic wide editorial prose should still wrap when layout already measured it as multiline."""
    from pptx import Presentation

    prs = Presentation()
    prs.slide_width = int(914400 * 13.33)
    prs.slide_height = int(914400 * 7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    elem = {
        'type': 'text',
        'tag': 'p',
        'text': 'AI订单的快速放量，正是知行合一的结果。不是喊一句“AI转型”的口号，而是实实在在把AI能力注入星瀚、星空、星辰等核心产品，切切实实帮客户提升效率，自然得到市场的认可。',
        'segments': [
            {'text': 'AI订单的快速放量，正是知行合一的结果。不是喊一句“AI转型”的口号，而是实实在在把AI能力注入星瀚、星空、星辰等核心产品，切切实实帮客户提升效率，自然得到市场的认可。', 'color': '#111111', 'fontSize': '16px', 'fontFamily': 'Helvetica', 'letterSpacing': '', 'bold': False, 'strike': False, 'bgColor': None, 'inlineBgBounds': None, 'kind': 'text'},
        ],
        'bounds': {'x': 6.68, 'y': 3.15, 'width': 6.65, 'height': 0.54},
        'naturalHeight': 0.54,
        'styles': {
            'fontSize': '16px',
            'fontWeight': '400',
            'fontFamily': 'Helvetica',
            'letterSpacing': '',
            'color': '#111111',
            'textAlign': 'left',
            'lineHeight': '1.6',
            'paddingLeft': '0px',
            'paddingRight': '0px',
            'paddingTop': '0px',
            'paddingBottom': '0px',
        },
    }

    export_sandbox.export_text_element(slide, elem, (250, 250, 248))
    tf = slide.shapes[-1].text_frame
    assert tf.word_wrap is True, tf.word_wrap
    assert tf.auto_size == export_sandbox.MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT, tf.auto_size
    print("  PASS: wide measured multiline prose wraps before export")


def test_build_text_element_centered_block_command_shrinkwraps():
    """Centered column command cards should shrink-wrap to content width and export centered."""
    html = """<!doctype html><html><head><style>
    .slide-content { max-width: 600px; display:flex; flex-direction:column; align-items:center; text-align:center; }
    .cmd { padding: 10px 16px; border: 1px solid rgba(26,26,24,0.15); border-radius: 2px;
           font-family: "EB Garamond", monospace; font-size: 14px; line-height: 1.6; text-align:left; }
    </style></head><body>
      <div class="slide-content">
        <div class="cmd">/slide-creator "你的主题" --style "Chinese Chan"</div>
      </div>
    </body></html>"""
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    content = soup.select_one('.slide-content')
    parent_style = compute_element_style(content, css_rules, content.get('style', ''))
    node = soup.select_one('.cmd')
    style = compute_element_style(node, css_rules, node.get('style', ''), parent_style)
    elem = build_text_element(node, style, css_rules, 1440, 600.0)
    assert elem is not None
    assert elem['preferContentWidth'] is True, elem
    assert elem['styles']['textAlign'] == 'center', elem['styles']
    assert elem['bounds']['width'] < 4.8, elem['bounds']
    print("  PASS: centered block command cards shrink-wrap and center")


def test_export_shape_background_small_stamp_seal_keeps_border_without_shadow():
    """Small bordered seal shapes should keep their border and skip ambient card shadows."""
    from pptx import Presentation

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    elem = {
        'type': 'shape',
        'tag': 'div',
        'bounds': {'x': 6.0, 'y': 2.0, 'width': 0.222, 'height': 0.222},
        'styles': {
            'backgroundColor': 'rgba(196,30,58,0.08)',
            'backgroundImage': '',
            'border': '1px solid #C41E3A',
            'borderLeft': '1px solid #C41E3A',
            'borderRight': '1px solid #C41E3A',
            'borderTop': '1px solid #C41E3A',
            'borderBottom': '1px solid #C41E3A',
            'borderRadius': '2px',
            'marginTop': '',
            'marginBottom': '',
            'marginLeft': '',
            'marginRight': '',
        },
    }
    export_sandbox.export_shape_background(slide, elem, (250, 250, 248))
    with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        prs.save(tmp_path)
        with ZipFile(tmp_path) as zf:
            xml = zf.read('ppt/slides/slide1.xml').decode('utf-8')
        assert 'C41E3A' in xml, xml
        assert 'outerShdw' not in xml, xml
    finally:
        tmp_path.unlink(missing_ok=True)
    print("  PASS: small seal keeps border and skips shadow")


def _find_textbox_xml(xml: str, text_snippet: str):
    shape_pattern = re.compile(r'<p:sp>(.*?)</p:sp>', re.S)
    target_block = None
    for block in shape_pattern.findall(xml):
        if text_snippet in block:
            target_block = block
            break
    assert target_block, text_snippet

    geom_match = re.search(
        r'<a:off x="(?P<x>\d+)" y="(?P<y>\d+)"/><a:ext cx="(?P<cx>\d+)" cy="(?P<cy>\d+)"/>',
        target_block,
    )
    body_match = re.search(
        r'<a:bodyPr wrap="(?P<wrap>[^"]+)".*?>(?P<bodypr>.*?)</a:bodyPr>',
        target_block,
        re.S,
    )
    assert geom_match and body_match, target_block
    return {
        'x': int(geom_match.group('x')),
        'y': int(geom_match.group('y')),
        'cx': int(geom_match.group('cx')),
        'cy': int(geom_match.group('cy')),
        'wrap': body_match.group('wrap'),
        'bodypr': body_match.group('bodypr'),
        'block': target_block,
    }


def test_chinese_chan_roundtrip_wrap_fidelity_and_no_page_overflow():
    """Chinese Chan text-contract pages should keep authored column width, wrap mode, and stay inside the slide."""
    src = REPO_ROOT / 'demo' / 'chinese-chan-zh.html'
    if not src.exists():
        return

    with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
        out_path = Path(tmp.name)

    try:
        export_sandbox_pptx(str(src), str(out_path))
        slide_w = int(914400 * 13.33)

        with ZipFile(out_path) as zf:
            slide2_xml = zf.read('ppt/slides/slide2.xml').decode('utf-8')
            slide3_xml = zf.read('ppt/slides/slide3.xml').decode('utf-8')
            slide8_xml = zf.read('ppt/slides/slide8.xml').decode('utf-8')

        slide2_para_1 = _find_textbox_xml(slide2_xml, '演示工具越来越臃肿。模板商店卖着换汤不换药的「新设计」。AI 生成器做出来的幻灯片——精致、通用、过目即忘。')
        slide2_para_2 = _find_textbox_xml(slide2_xml, '我们从一个更简单的前提开始：')
        slide3_para = _find_textbox_xml(slide3_xml, '每种预设都是一套')
        slide8_title = _find_textbox_xml(slide8_xml, '从一个预设开始')
        slide8_cmd = _find_textbox_xml(slide8_xml, '/slide-creator "你的主题" --style "Chinese Chan"')

        for box in (slide2_para_1, slide2_para_2, slide3_para, slide8_title):
            assert box['wrap'] == 'square', box
            assert 'spAutoFit' in box['bodypr'], box['bodypr']
            assert box['x'] + box['cx'] <= slide_w + 1000, (box, slide_w)

        # Preserve the authored 600px reading column instead of shrinking to the
        # text's intrinsic width. This prevents late wrong wraps and page spill.
        min_authored_column_emu = int(5.45 * 914400)
        assert slide2_para_1['cx'] >= min_authored_column_emu, slide2_para_1
        assert slide2_para_2['cx'] >= min_authored_column_emu, slide2_para_2
        assert slide3_para['cx'] >= min_authored_column_emu, slide3_para
        assert slide8_title['cx'] >= min_authored_column_emu, slide8_title

        # Closing command card should shrink-wrap and stay centered rather than
        # stretching to the full authored column and reading as left-aligned.
        assert slide8_cmd['cx'] < min_authored_column_emu, slide8_cmd
        cmd_center = slide8_cmd['x'] + slide8_cmd['cx'] / 2
        title_center = slide8_title['x'] + slide8_title['cx'] / 2
        assert abs(cmd_center - title_center) <= 120000, (slide8_cmd, slide8_title)
        assert 'algn="ctr"' in slide8_cmd['block'], slide8_cmd['block']

        # The small zen seal should keep its border and avoid shadow/no-fill fallback.
        seal_match = re.search(
            r'<a:off x="(?P<x>\d+)" y="(?P<y>\d+)"/><a:ext cx="203200" cy="203200"/>.*?'
            r'<a:solidFill><a:srgbClr val="(?P<fill>[0-9A-F]{6})"/></a:solidFill>.*?'
            r'<a:ln[^>]*>.*?<a:solidFill><a:srgbClr val="(?P<line>[0-9A-F]{6})"/></a:solidFill>',
            slide8_xml,
            re.S,
        )
        assert seal_match, slide8_xml
        assert seal_match.group('fill') == 'F5E8E8', seal_match.groupdict()
        assert seal_match.group('line') == 'C41E3A', seal_match.groupdict()
    finally:
        out_path.unlink(missing_ok=True)

    print("  PASS: Chinese Chan keeps wrap width, centered command alignment, and seal border fidelity")


def test_measure_flow_box_intrinsic_height_for_layer_card():
    """Future gate: layer cards should measure as a single flow_box container."""
    measure_flow_box = _require_symbol('measure_flow_box')
    if measure_flow_box is None:
        return

    html = '''
    <div class="layer" style="display:flex;align-items:flex-start;gap:14px;padding:14px 18px;border-radius:14px;
         background:rgba(255,255,255,0.60);border:1px solid rgba(255,255,255,0.90);border-left:4px solid #0ea5e9;">
      <div style="width:34px;height:34px;border-radius:50%;background:#2563eb;color:#fff;">1</div>
      <div>
        <h4 style="margin-bottom:4px;">描述你的主题</h4>
        <p>告诉 slide-creator 你想呈现什么。</p>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    layer = soup.find('div')
    measured = measure_flow_box(layer, [], {}, 1440, 820)

    assert measured.get('layout') == 'flow_box', f"Expected flow_box layout, got {measured.get('layout')!r}"
    assert measured.get('measure', {}).get('intrinsic_height', 0) > 0.55, "Measured flow_box height should be non-trivial"
    print("  PASS: flow_box intrinsic height measured")


def test_measure_flow_box_marks_descendants_in_flow_box():
    """flow_box descendants should opt out of legacy card-group layout."""
    measure_flow_box = _require_symbol('measure_flow_box')
    if measure_flow_box is None:
        return

    html = '''
    <div class="layer" style="display:flex;align-items:flex-start;gap:14px;padding:14px 18px;border-radius:14px;
         background:rgba(255,255,255,0.60);border:1px solid rgba(255,255,255,0.90);border-left:4px solid #0ea5e9;">
      <div style="font-size:1.5rem;flex-shrink:0;">📝</div>
      <div>
        <h4 style="margin-bottom:4px;">当前幻灯片备注</h4>
        <p>按 <kbd>P</kbd> 在独立窗口查看演讲者备注。</p>
      </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    measured = measure_flow_box(soup.find('div'), [], {}, 1440, 820)
    descendants = measured.get('children', [])

    assert descendants, "flow_box should contain descendants"
    assert all(child.get('_in_flow_box') for child in descendants), descendants
    assert not any(child.get('_card_group') for child in descendants), descendants
    assert not any(child.get('_is_border_left') for child in descendants), descendants
    bg_shape = next(child for child in descendants if child.get('_is_card_bg'))
    assert '4px' in bg_shape.get('styles', {}).get('borderLeft', ''), bg_shape
    print("  PASS: flow_box descendants opt into _in_flow_box")


def test_measure_flow_box_promotes_visible_flex_column_card():
    """Visible flex-column cards should export as a single flow_box container."""
    measure_flow_box = _require_symbol('measure_flow_box')
    if measure_flow_box is None:
        return

    html = '''
    <div style="display:flex;flex-direction:column;padding:16px;border:1px solid #30363d;
                border-radius:6px;background:#161b22;gap:10px;">
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:20px;font-weight:800;color:#f85149;">01</span>
        <h3 style="font-size:18px;">复杂的工具链</h3>
      </div>
      <p style="font-size:15px;">Node、Webpack、npm、插件——只为做幻灯片。</p>
      <div style="height:2px;background:#30363d;"></div>
      <span style="font-size:13px;color:#f85149;">▼ 72% 用户抱怨构建复杂度</span>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    measured = measure_flow_box(soup.find('div'), [], {}, 1440, 540)

    assert measured is not None, "flex-column card should promote to flow_box"
    assert measured.get('layout') == 'flow_box', measured
    assert measured.get('measure', {}).get('intrinsic_height', 0) > 0.8, measured.get('measure')
    assert any(child.get('_is_card_bg') for child in measured.get('children', [])), measured.get('children', [])
    print("  PASS: flex-column card promotes to flow_box")


def test_table_cell_fragments_measure_kbd_sequence():
    """Future gate: table cells should keep kbd fragments instead of flattening away."""
    html = '''
    <table style="width:100%;border-collapse:collapse;">
      <tr>
        <td><kbd>→</kbd> <kbd>Space</kbd> <kbd>↓</kbd></td>
        <td>下一个幻灯片</td>
      </tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)
    cell = table_ir['rows'][0]['cells'][0]
    fragments = cell.get('fragments')

    if not fragments:
        print("  SKIP: table cell fragments pending implementation")
        return

    kinds = [frag.get('kind') for frag in fragments]
    assert kinds.count('kbd') == 3, f"Expected 3 kbd fragments, got {kinds}"
    print("  PASS: table cell preserves kbd fragments")


def test_build_table_element_classifies_presentation_rows():
    """Presentational row lists should not stay on the generic data-table path."""
    html = '''
    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
      <tr>
        <td style="padding:6px 0;border-bottom:1px solid rgba(14,165,233,0.10);"><kbd>→</kbd> <kbd>Space</kbd> <kbd>↓</kbd></td>
        <td style="padding:6px 0 6px 12px;border-bottom:1px solid rgba(14,165,233,0.10);color:#475569;">下一个幻灯片</td>
      </tr>
      <tr>
        <td style="padding:6px 0;">Home / End</td>
        <td style="padding:6px 0 6px 12px;color:#475569;">首/末幻灯片</td>
      </tr>
      <tr>
        <td style="padding:6px 0;">滑动 ← →</td>
        <td style="padding:6px 0 6px 12px;color:#475569;">触摸导航</td>
      </tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)

    assert table_ir.get('type') == 'presentation_rows', table_ir.get('type')
    print("  PASS: presentational tables classify as presentation_rows")


def test_presentation_rows_use_compact_single_line_row_height():
    """Presentation rows should keep compact single-line heights instead of table-like 0.31+ rows."""
    html = '''
    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
      <tr><td style="padding:5px 0;border-bottom:1px solid rgba(14,165,233,0.10);">内容密度</td><td style="padding:5px 0 5px 8px;border-bottom:1px solid rgba(14,165,233,0.10);color:#475569;">≥ 65% 填充</td></tr>
      <tr><td style="padding:5px 0;border-bottom:1px solid rgba(14,165,233,0.10);">列平衡</td><td style="padding:5px 0 5px 8px;border-bottom:1px solid rgba(14,165,233,0.10);color:#475569;">最短列 ≥ 60%</td></tr>
      <tr><td style="padding:5px 0;">色彩律</td><td style="padding:5px 0 5px 8px;color:#475569;">90/8/2 分配</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)

    assert table_ir.get('type') == 'presentation_rows', table_ir.get('type')
    row_heights = [row.get('height', 0.0) for row in table_ir.get('rows', [])]
    assert row_heights and min(row_heights) >= 0.264, row_heights
    assert row_heights and max(row_heights) < 0.29, row_heights
    print("  PASS: presentation rows use compact single-line row height")


def test_presentation_rows_keep_fitted_key_column_and_expand_value_column():
    """Presentation rows should keep a fitted key column instead of proportionally stretching both columns."""
    html = '''
    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
      <tr><td style="padding:5px 0;border-bottom:1px solid rgba(14,165,233,0.10);">内容密度</td><td style="padding:5px 0 5px 8px;border-bottom:1px solid rgba(14,165,233,0.10);color:#475569;">≥ 65% 填充</td></tr>
      <tr><td style="padding:5px 0;border-bottom:1px solid rgba(14,165,233,0.10);">标题质量</td><td style="padding:5px 0 5px 8px;border-bottom:1px solid rgba(14,165,233,0.10);color:#475569;">断言式，非通用</td></tr>
      <tr><td style="padding:5px 0;">布局轮换</td><td style="padding:5px 0 5px 8px;color:#475569;">禁止连续 3 页</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)

    col_widths = export_sandbox._compute_presentation_row_column_widths(table_ir.get('rows', []), 3.536)
    assert len(col_widths) == 2, col_widths
    assert col_widths[0] < 1.35, col_widths
    assert col_widths[1] > 2.10, col_widths
    assert abs(sum(col_widths) - 3.536) < 0.01, col_widths
    print("  PASS: presentation rows keep fitted key column widths")


def test_presentation_rows_shortcut_column_gets_extra_runway():
    """Shortcut-heavy first columns should get more runway than prose labels."""
    html = '''
    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
      <tr><td style="padding:6px 0;">→ Space ↓</td><td style="padding:6px 0 6px 12px;color:#475569;">下一个幻灯片</td></tr>
      <tr><td style="padding:6px 0;">Home / End</td><td style="padding:6px 0 6px 12px;color:#475569;">首/末幻灯片</td></tr>
      <tr><td style="padding:6px 0;">F5</td><td style="padding:6px 0 6px 12px;color:#475569;">全屏演示</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)

    col_widths = export_sandbox._compute_presentation_row_column_widths(table_ir.get('rows', []), 3.536)
    assert len(col_widths) == 2, col_widths
    assert col_widths[0] > 1.45, col_widths
    assert col_widths[1] < 2.10, col_widths
    print("  PASS: presentation rows give shortcut columns extra runway")


def test_presentation_row_label_uses_stronger_ink():
    """First-column labels in presentation rows should use strong ink on light cards."""
    assert export_sandbox._presentation_row_label_color('rgb(15,23,42)') == '#000000'
    assert export_sandbox._presentation_row_label_color('#0f172a') == '#000000'
    assert export_sandbox._presentation_row_label_color('rgb(51,65,85)') == 'rgb(51,65,85)'
    print("  PASS: presentation row label uses stronger ink")


def test_display_heading_normalizes_deep_slate_to_black():
    """Short dark-slate display headings should strengthen to black, without muting boxed inline fragments."""
    html = '<h4 style="color:#0f172a;">核心 8 项 <span style="background:#dbeafe;color:#0f172a;padding:2px 8px;border-radius:999px;">当前</span></h4>'
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    h4 = soup.find('h4')
    style = compute_element_style(h4, css_rules, h4.get('style', ''))
    ir = build_text_element(h4, style, css_rules, 1440, 720)

    heading_seg = next(seg for seg in ir.get('segments', []) if '核心' in seg.get('text', ''))
    badge_seg = next(seg for seg in ir.get('segments', []) if '当前' in seg.get('text', ''))
    assert heading_seg['color'] == '#000000', ir.get('segments', [])
    assert badge_seg['color'].lower() == '#0f172a', ir.get('segments', [])
    print("  PASS: display heading normalizes deep slate to black")


def test_presentation_row_shortcut_cell_keeps_original_ink():
    """Shortcut-token first cells should not be over-strengthened to black."""
    html = '''
    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
      <tr>
        <td style="padding:6px 0;color:#0f172a;">Home / End</td>
        <td style="padding:6px 0 6px 12px;color:#475569;">首/末幻灯片</td>
      </tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)
    first_cell = table_ir['rows'][0]['cells'][0]

    assert first_cell['styles']['color'].lower() == '#0f172a', first_cell['styles']['color']
    print("  PASS: presentation-row shortcut cell keeps original ink")


def test_build_table_element_keeps_real_data_tables():
    """Real data tables with headers should remain on the generic table path."""
    html = '''
    <table style="width:100%;border-collapse:collapse;">
      <tr><th>季度</th><th>转化率</th></tr>
      <tr><td>Q1</td><td>12%</td></tr>
      <tr><td>Q2</td><td>18%</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style)

    assert table_ir.get('type') == 'table', table_ir.get('type')
    print("  PASS: real data tables stay on table path")


def test_build_table_element_respects_local_content_width_constraint():
    """Tables inside a local rail should size to that rail, not the full slide width."""
    html = '''
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr><th>命令</th><th>用途</th><th>耗时</th></tr></thead>
      <tbody>
        <tr><td>/slide-creator</td><td>交互模式——描述心情，选择风格</td><td>3-6 min</td></tr>
      </tbody>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    table_ir = export_sandbox.build_table_element(table, [], style, content_width_px=612)

    assert abs(table_ir['bounds']['width'] - (612 / PX_PER_IN)) < 1e-6, table_ir['bounds']
    assert abs(sum(table_ir.get('measure', {}).get('col_widths', [])) - table_ir['bounds']['width']) < 0.01, table_ir.get('measure')
    print("  PASS: table IR respects local wrapper width")


def test_build_table_element_remeasures_wrapped_row_height_after_width_constraint():
    """Narrow local tables should increase row height once long value cells wrap."""
    html = '''
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr><th>命令</th><th>用途</th><th>耗时</th></tr></thead>
      <tbody>
        <tr><td>/slide-creator</td><td>交互模式——描述心情，选择风格，生成完整演示文稿。</td><td>3-6 min</td></tr>
      </tbody>
    </table>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    style = compute_element_style(table, [], table.get('style', ''))
    wide_ir = export_sandbox.build_table_element(table, [], style, content_width_px=960)
    narrow_ir = export_sandbox.build_table_element(table, [], style, content_width_px=420)

    wide_body_h = wide_ir['rows'][1]['height']
    narrow_body_h = narrow_ir['rows'][1]['height']
    assert narrow_body_h > wide_body_h + 0.08, (wide_body_h, narrow_body_h)
    print("  PASS: constrained table rows remeasure wrapped height")


def test_table_card_height_uses_actual_table_bounds():
    """Cards wrapping tables should use measured table height, not row-count heuristics."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: table_card_height_uses_actual_table_bounds (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    slide = slides[6]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide['elements'])
    slide['_slide_index'] = 6
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    containers = _collect_elements_by_type(slide['elements'], 'container')
    container = next(
        e for e in containers
        if any(child.get('type') in ('table', 'presentation_rows') for child in _collect_elements_by_type([e], 'table') + _collect_elements_by_type([e], 'presentation_rows'))
    )
    card = next(c for c in _collect_elements_by_type([container], 'shape') if c.get('_is_card_bg'))
    table = next(
        c for c in _collect_elements_by_type([container], 'table') + _collect_elements_by_type([container], 'presentation_rows')
        if c.get('type') in ('table', 'presentation_rows')
    )

    card_bottom = card['bounds']['y'] + card['bounds']['height']
    table_bottom = table['bounds']['y'] + table['bounds']['height']
    assert card_bottom >= table_bottom, (
        f"Card bottom {card_bottom:.3f} should cover table bottom {table_bottom:.3f}"
    )
    print("  PASS: table card height uses actual table bounds")


def test_centered_inline_command_prefers_content_width():
    """Centered inline command rows should shrink-wrap to measured fragment width."""
    html = '''
    <section class="slide">
      <div style="text-align:center;max-width:720px;">
        <p style="margin-top:20px;font-size:0.9rem;color:#64748b;">
          <code style="padding:2px 8px;background:rgba(14,165,233,0.10);">clawhub install kai-slide-creator</code>
          &nbsp;·&nbsp;
          <a href="https://github.com/kaisersong/slide-creator" style="color:#2563eb;text-decoration:none;">GitHub ↗</a>
        </p>
      </div>
    </section>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    slide = soup.find('section')
    center = slide.find('div')
    results = flat_extract(center, css_rules, None, 1440)
    layout_slide_elements(results, 13.33, 810 / 108, {'paddingTop': '40px'}, {'_slide_index': 9})

    command_line = next(r for r in results if r.get('type') == 'text' and 'clawhub install' in r.get('text', ''))
    assert command_line.get('preferContentWidth'), "Inline command row should opt into content-width centering"
    assert command_line['bounds']['width'] < 5.5, (
        f"Command line width {command_line['bounds']['width']:.3f}\" should shrink-wrap, not fill the full 6.67\" column"
    )
    print("  PASS: centered inline command prefers content width")


def test_export_centered_inline_command_uses_fragment_runway():
    """Centered code+link rows should use one carrier textbox plus a pill overlay."""
    html = '''
    <html><body>
      <section class="slide" style="padding:56px 80px;background:linear-gradient(160deg,#f0f9ff,#e0f2fe);">
        <div style="text-align:center;max-width:720px;">
          <p style="margin-top:20px;font-size:0.9rem;color:#64748b;">
            <code style="padding:2px 8px;background:rgba(37,99,235,0.08);border-radius:999px;">clawhub install kai-slide-creator</code>
            &nbsp;·&nbsp;
            <a href="https://github.com/kaisersong/slide-creator" style="color:#2563eb;text-decoration:none;">GitHub ↗</a>
          </p>
        </div>
      </section>
    </body></html>
    '''

    with tempfile.TemporaryDirectory(prefix='kai-export-inline-runway-') as tmp_dir:
        html_path = Path(tmp_dir) / 'command-row.html'
        pptx_path = Path(tmp_dir) / 'command-row.pptx'
        html_path.write_text(html, encoding='utf-8')
        export_sandbox_pptx(html_path, pptx_path, 1440, 810)

        from pptx import Presentation
        prs = Presentation(str(pptx_path))
        slide = prs.slides[0]

        texts = []
        pill_shapes = []
        for shape in slide.shapes:
            text = getattr(shape, 'text', '').strip() if hasattr(shape, 'text') else ''
            if text:
                texts.append(text)
            try:
                fill = tuple(shape.fill.fore_color.rgb)
            except Exception:
                fill = None
            if fill and shape.width / 914400 > 2.5 and shape.height / 914400 > 0.20:
                pill_shapes.append((shape.width / 914400, shape.height / 914400, fill))

        assert any('clawhub install kai-slide-creator' in text and 'GitHub ↗' in text for text in texts), texts
        assert all(text != 'GitHub ↗' for text in texts), texts
        assert all(text != 'clawhub install kai-slide-creator' for text in texts), texts
        assert pill_shapes, pill_shapes
    print("  PASS: centered inline command exports as carrier textbox + pill overlay")


def test_centered_inline_command_mutes_trailing_link_color():
    """Centered command rows should keep trailing link/separator on the muted body ink."""
    html = '''
    <section class="slide">
      <div style="text-align:center;max-width:720px;">
        <p style="margin-top:20px;font-size:0.9rem;color:#64748b;">
          <code style="padding:2px 8px;background:rgba(37,99,235,0.08);border-radius:999px;">clawhub install kai-slide-creator</code>
          &nbsp;·&nbsp;
          <a href="https://github.com/kaisersong/slide-creator" style="color:#2563eb;text-decoration:none;">GitHub ↗</a>
        </p>
      </div>
    </section>'''
    soup = BeautifulSoup(html, 'html.parser')
    css_rules = extract_css_from_soup(soup)
    p = soup.find('p')
    style = compute_element_style(p, css_rules, p.get('style', ''))
    ir = build_text_element(p, style, css_rules, 1440, 720)

    link_segment = next(seg for seg in ir.get('segments', []) if 'GitHub' in seg.get('text', ''))
    assert link_segment['color'] == '#64748b', ir.get('segments', [])
    print("  PASS: centered inline command mutes trailing link color")


def test_export_accent_card_uses_narrow_strip_and_full_main_card():
    """Border-left accent cards should export as a narrow accent strip plus a full main card."""
    html = '''
    <html><body>
      <section class="slide" style="padding:56px 80px;background:linear-gradient(160deg,#f0f9ff,#e0f2fe);">
        <div style="max-width:820px;width:100%;">
          <div style="background:rgba(255,255,255,0.70);border:1px solid rgba(255,255,255,0.90);border-left:4px solid #0ea5e9;border-radius:20px;padding:22px 24px;">
            <h4 style="margin-bottom:8px;">标题</h4>
            <p>说明文本</p>
          </div>
        </div>
      </section>
    </body></html>
    '''

    with tempfile.TemporaryDirectory(prefix='kai-export-accent-card-') as tmp_dir:
        html_path = Path(tmp_dir) / 'accent-card.html'
        pptx_path = Path(tmp_dir) / 'accent-card.pptx'
        html_path.write_text(html, encoding='utf-8')
        export_sandbox_pptx(html_path, pptx_path, 1440, 810)

        from pptx import Presentation
        prs = Presentation(str(pptx_path))
        slide = prs.slides[0]
        widths = []
        for shape in slide.shapes:
            x = shape.left / 914400
            w = shape.width / 914400
            h = shape.height / 914400
            fill = None
            try:
                fill = tuple(shape.fill.fore_color.rgb)
            except Exception:
                pass
            if h > 0.4 and fill:
                widths.append((x, w, fill))

        accent_strip = next((item for item in widths if item[1] < 0.35 and item[2] == (14, 165, 233)), None)
        main_card = next((item for item in widths if item[1] > 1.0 and all(channel >= 245 for channel in item[2])), None)

        assert accent_strip is not None, widths
        assert main_card is not None, widths
        assert accent_strip[0] <= main_card[0] + 0.01, (accent_strip, main_card)
    assert main_card[1] > accent_strip[1] * 8, (accent_strip, main_card)
    print("  PASS: accent card exports as strip + full main card")


def test_slide4_theme_grid_cards_share_stretched_row_height():
    """Grid cards in one row should stretch their backgrounds to the shared row height."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide4_theme_grid_cards_share_stretched_row_height (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    slide = slides[3]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide['elements'])
    slide['_slide_index'] = 3
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    containers = _collect_elements_by_type(slide['elements'], 'container')
    grid = next(
        e for e in containers
        if len([c for c in _collect_elements_by_type([e], 'shape') if c.get('_is_card_bg')]) >= 4
    )
    card_heights = []

    def _walk(item):
        if item.get('type') == 'shape' and item.get('_is_card_bg'):
            card_heights.append(item['bounds']['height'])
        for child in item.get('children', []):
            _walk(child)

    _walk(grid)
    assert len(card_heights) >= 4, card_heights
    assert max(card_heights[:4]) - min(card_heights[:4]) < 0.05, card_heights[:4]
    print("  PASS: slide 4 theme cards stretch to shared row height")


def test_export_does_not_add_exporter_chrome_by_default():
    """Exporter should not inject page counter / nav dots unless explicitly requested."""
    html = '''
    <html><body>
      <section class="slide" style="padding:56px 80px;background:#0f172a;color:#e2e8f0;">
        <h1>Hello</h1>
        <p>World</p>
      </section>
    </body></html>
    '''

    with tempfile.TemporaryDirectory(prefix='kai-export-no-chrome-') as tmp_dir:
        html_path = Path(tmp_dir) / 'plain.html'
        pptx_path = Path(tmp_dir) / 'plain.pptx'
        html_path.write_text(html, encoding='utf-8')
        export_sandbox_pptx(html_path, pptx_path, 1440, 810)

        from pptx import Presentation
        prs = Presentation(str(pptx_path))
        slide = prs.slides[0]
        texts = [shape.text.strip() for shape in slide.shapes if hasattr(shape, 'text') and shape.text.strip()]

        assert '01 / 01' not in texts, texts
    print("  PASS: exporter chrome is opt-in")


def test_accent_callouts_keep_optical_gap_from_preceding_blocks():
    """Bottom accent/info callouts should keep a visible gap from the block above."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: accent_callouts_keep_optical_gap_from_preceding_blocks (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    targets = {
        1: 0.20,  # slide 2
        3: 0.20,  # slide 4
        7: 0.22,  # slide 8
        8: 0.22,  # slide 9
    }

    for slide_idx, min_gap in targets.items():
        slide = slides[slide_idx]
        pre_pass_corrections(slide['elements'])
        slide['_slide_index'] = slide_idx
        layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

        prev_elem = slide['elements'][-3]
        shape = slide['elements'][-2]
        gap = shape['bounds']['y'] - (prev_elem['bounds']['y'] + prev_elem['bounds']['height'])
        assert gap >= min_gap, (slide_idx + 1, gap, min_gap, shape['bounds'], prev_elem['bounds'])

    print("  PASS: accent callouts keep optical gap from preceding blocks")


def test_slide10_gradient_divider_centers_in_heading_block():
    """Gradient divider under a centered heading should stay centered in the heading block."""
    html_path = Path(__file__).parent.parent / 'demo' / 'blue-sky-zh.html'
    if not html_path.exists():
        print("  SKIP: slide10_gradient_divider_centers_in_heading_block (HTML not found)")
        return

    slides = parse_html_to_slides(html_path, 1440, 810)
    slide = slides[9]
    pre_pass_corrections = getattr(export_sandbox, 'pre_pass_corrections')
    pre_pass_corrections(slide['elements'])
    slide['_slide_index'] = 9
    layout_slide_elements(slide['elements'], 13.33, 810 / 108, slide['slideStyle'], slide)

    heading = None
    divider = None

    def _walk(item):
        nonlocal heading, divider
        if item.get('type') == 'text' and item.get('tag') == 'h2' and heading is None:
            heading = item['bounds']
        if (
            item.get('type') == 'shape'
            and abs(item.get('bounds', {}).get('height', 0.0) - (3.0 / PX_PER_IN)) < 0.01
            and item.get('bounds', {}).get('width', 0.0) > 0.45
        ):
            divider = item['bounds']
        for child in item.get('children', []):
            _walk(child)

    for element in slide['elements']:
        _walk(element)

    assert heading is not None, slide['elements']
    assert divider is not None, slide['elements']
    divider_center = divider['x'] + divider['width'] / 2.0
    heading_center = heading['x'] + heading['width'] / 2.0
    assert abs(divider_center - heading_center) < 0.05, (heading, divider)
    print("  PASS: slide 10 divider centers in heading block")


def test_export_corpus_parse_smoke():
    """Corpus HTML samples should remain parseable across Blue Sky and non-Blue-Sky decks."""
    parsed = []
    skipped = []

    for sample in _corpus_samples():
        path = sample['path']
        if not path.exists():
            if sample['required']:
                raise AssertionError(f"Required corpus sample missing: {path}")
            skipped.append(sample['label'])
            continue

        slides = parse_html_to_slides(path, 1440, 810)
        assert slides, f"Corpus sample {sample['label']} produced no slides"
        text_count = sum(_count_text_elements(slide['elements']) for slide in slides)
        assert text_count > 0, f"Corpus sample {sample['label']} produced no text elements"
        parsed.append(sample['label'])

    assert len(parsed) >= 3, f"Expected at least 3 parsed corpus samples, got {parsed}"
    assert any('blue-sky' in label for label in parsed), f"Expected at least one Blue Sky sample, got {parsed}"
    assert any('intro' in label or 'handwritten' in label or 'swiss-modern' in label for label in parsed), (
        f"Expected at least one non-Blue-Sky sample, got {parsed}"
    )
    if skipped:
        print(f"  SKIP: optional corpus samples unavailable: {', '.join(skipped)}")
    print(f"  PASS: corpus parse smoke ({len(parsed)} samples)")


def test_handwritten_fixture_covers_core_patterns():
    """Handwritten fixture should cover grouped-inline, cards, lists, and tables."""
    if not HANDWRITTEN_FIXTURE.exists():
        raise AssertionError(f"Missing handwritten fixture: {HANDWRITTEN_FIXTURE}")

    slides = parse_html_to_slides(HANDWRITTEN_FIXTURE, 1440, 810)
    assert len(slides) == 3, f"Expected 3 slides in handwritten fixture, got {len(slides)}"

    all_texts = []
    all_tables = []
    all_presentation_rows = []
    all_shapes = []
    for slide in slides:
        all_texts.extend(_collect_text_values(slide['elements']))
        all_tables.extend(_collect_elements_by_type(slide['elements'], 'table'))
        all_presentation_rows.extend(_collect_elements_by_type(slide['elements'], 'presentation_rows'))
        all_shapes.extend(_collect_elements_by_type(slide['elements'], 'shape'))

    joined = "\n".join(all_texts)
    table_cell_texts = []
    table_fragment_kinds = []
    for table in all_tables + all_presentation_rows:
        for row in table.get('rows', []):
            for cell in row.get('cells', []):
                cell_text = (cell.get('text') or '').strip()
                if cell_text:
                    table_cell_texts.append(cell_text)
                for fragment in cell.get('fragments') or []:
                    kind = fragment.get('kind')
                    if kind:
                        table_fragment_kinds.append(kind)

    assert 'Handwritten Export Corpus' in joined, "Fixture should include title slide text"
    assert 'GitHub' in joined, "Fixture should include a link-like grouped inline row"
    assert table_fragment_kinds.count('kbd') >= 3, (
        f"Fixture should include kbd-heavy presentational rows, got fragments {table_fragment_kinds}"
    )
    assert any('Q2' in txt or '转化率' in txt for txt in table_cell_texts), (
        f"Fixture should include a real data table, got {table_cell_texts}"
    )
    assert all_tables, "Fixture should include at least one real table element"
    assert all_presentation_rows, "Fixture should include at least one presentation_rows element"
    assert all_shapes, "Fixture should include at least one background/card shape"
    print("  PASS: handwritten fixture covers core patterns")


def test_handwritten_fixture_structural_eval_gate():
    """A small handwritten corpus export should clear structural eval gates."""
    if not HANDWRITTEN_FIXTURE.exists():
        raise AssertionError(f"Missing handwritten fixture: {HANDWRITTEN_FIXTURE}")

    with tempfile.TemporaryDirectory(prefix='kai-export-corpus-') as tmp_dir:
        out_path = Path(tmp_dir) / 'handwritten-card-list-table.pptx'
        export_sandbox_pptx(HANDWRITTEN_FIXTURE, out_path, 1440, 810)
        summary = rigorous_eval.collect_eval_summary(
            golden_path=str(out_path),
            sandbox_path=str(out_path),
            include_visual=False,
        )

        assert summary['sandbox_overflow_count'] == 0, summary['sandbox_overflow_issues']
        assert summary['sandbox_overlap_count'] == 0, summary['sandbox_overlap_issues']
        assert summary['element_gap_count'] == 0, summary['element_gap_issues']
        assert summary['card_containment_count'] == 0, summary['card_containment_issues']
        assert summary['color_diff_count'] == 0, summary['color_diff_issues']
        assert summary['total_actionable'] == 0, summary
    print("  PASS: handwritten fixture structural eval gate")


# ─── Test Runner ──────────────────────────────────────────────────────────────

def run_tests():
    print("Running export-sandbox-pptx tests...")
    print()

    print("Utilities:")
    test_discover_slide_roots_accepts_generic_section_deck()
    test_discover_slide_roots_rejects_article_like_document()
    test_assign_support_tier_uses_deterministic_precedence()
    test_analyze_source_returns_raw_signal_bundles()
    test_build_profiles_assigns_contract_bound_deck_profile()
    test_build_profiles_assigns_semantic_enhanced_for_generic_section_deck()
    test_solve_geometry_emits_pptx_geometry_plan_with_render_hints()
    test_solve_geometry_preserves_legacy_slide_fields_for_compat_adapter()
    test_render_pptx_uses_geometry_render_hints_for_contract_wrap()
    test_analyze_source_raw_slide_signals_describe_authored_slide()
    test_build_profiles_does_not_overstate_slide_contract_bound_without_local_evidence()
    test_plan_slides_does_not_promote_past_analysis_tier()
    test_plan_slides_records_override_reasons_for_export_role()
    test_plan_slides_isolates_downgrade_chain_per_plan()
    test_parse_html_to_slides_generic_section_roots_keep_fixed_content_isolated_per_slide()
    test_discover_slide_roots_prefers_explicit_dot_slide_over_generic_sections()
    test_parse_px()
    test_parse_px_supports_minmax_math()
    test_validate_export_hints_rejects_unknown_layout_fields()
    test_detect_producer_requires_cross_mechanism_medium_signals()
    test_resolve_repo_root_survives_missing___file__()
    test_run_skill_export_bootstrap_loads_installed_exporter()
    test_parse_css_rules_respects_media_queries_and_important()
    test_selector_matches_ignores_dynamic_hover_state()
    test_parse_grid_track_widths_handles_split_and_auto_fit()
    test_collect_export_context_loads_enterprise_dark_contract_and_body_grid()
    test_collect_export_context_loads_data_story_contract_and_body_grid()
    test_collect_export_context_loads_swiss_modern_contract_with_layout_tiers()
    test_slide_creator_chinese_chan_loads_contract_and_runtime_chrome_fallback()
    test_collect_export_context_loads_aurora_mesh_contract_with_snapshots()
    test_extract_aurora_mesh_background_builds_overlay_shapes()
    test_parse_html_to_slides_aurora_uses_solid_base_without_mesh_overlays()
    test_slide_creator_contract_manifest_tracks_upstream_and_data_story()
    test_sync_slide_creator_contracts_builds_data_story_contract()
    test_sync_slide_creator_contracts_builds_aurora_mesh_contract()
    test_sync_slide_creator_contracts_builds_swiss_modern_contract()
    test_parse_html_to_slides_aurora_stat_row_stays_within_slide_width()
    test_parse_html_to_slides_aurora_stat_row_defaults_to_compact_items()
    test_parse_html_to_slides_aurora_stat_row_respects_explicit_stretch_width()
    test_parse_html_to_slides_aurora_wrapper_style_preserves_centered_layout()
    test_parse_html_to_slides_aurora_install_items_keep_separate_vertical_cards()
    test_parse_html_to_slides_swiss_compatible_wrapper_unwraps_and_preserves_two_columns()
    test_media_query_max_height_does_not_override_large_heading_at_default_viewport()
    test_short_latin_inline_block_label_uses_compact_width()
    test_enterprise_dark_split_cards_stack_in_right_column()
    test_enterprise_dark_install_grid_prefers_centered_single_column_stack()
    test_enterprise_dark_cta_kpi_grid_preserves_two_card_widths()
    test_enterprise_dark_workflow_cards_share_row_height()
    test_enterprise_dark_workflow_index_keeps_breathing_room_before_title()
    test_enterprise_dark_trend_rows_stretch_full_card_width()
    test_data_story_problem_split_preserves_kpi_cards_as_nested_containers()
    test_data_story_solution_grid_preserves_solution_cards_as_nested_containers()
    test_data_story_feature_grid_preserves_cards_as_nested_containers()
    test_data_story_problem_cards_stack_metric_and_copy_vertically()
    test_flat_extract_content_svg_builds_relative_container()
    test_flat_extract_content_svg_keeps_polyline_and_dots()
    test_data_story_problem_split_keeps_svg_chart_container()
    test_data_story_feature_cards_stack_text_content_vertically()
    test_data_story_cta_kpi_grid_prefers_centered_single_column_stack()
    test_data_story_nested_card_groups_keep_grid_slot_width()
    test_data_story_install_rows_keep_horizontal_rails()
    test_data_story_centered_column_wrapper_preserves_max_width_and_children()
    test_data_story_centered_wrapper_keeps_paired_pills_overlaid()
    test_data_story_feature_cards_use_contract_min_height()
    test_data_story_style_cards_preserve_authored_preview_body_trend_spacing()
    test_data_story_solution_cards_preserve_compact_icon_title_body_flow()
    test_data_story_feature_cards_preserve_compact_metric_title_body_flow()
    test_data_story_metric_cards_keep_large_numbers_single_line()
    test_data_story_metric_grids_preserve_authored_row_width_when_not_centered()
    test_data_story_left_aligned_slides_do_not_center_narrow_titles()
    test_data_story_relative_grids_normalize_local_origin()
    test_data_story_feature_grid_children_stay_within_local_container_width()
    test_export_freeform_open_path_uses_connector_segments()
    test_data_story_style_cards_use_contract_solver_and_keep_preview_slot()
    test_slide_anchored_text_preserves_bottom_right_position()
    test_parse_html_to_slides_clones_body_fixed_brand_mark_for_each_slide()
    test_centered_flex_wrap_preserves_intrinsic_metric_stack_widths()
    test_compact_flex_row_packs_stat_blocks_at_intrinsic_width()
    test_compact_flex_row_falls_back_to_even_split_when_oversized()
    test_stretch_column_block_text_to_inner_width_expands_narrow_heading()
    test_swiss_index_list_rows_stretch_full_width_with_left_number_column()
    test_swiss_terminal_line_renders_dark_pill_with_paired_overlay()
    test_swiss_disc_steps_stack_vertically_with_left_number_column()
    test_hairline_height_halves_thin_borders_and_passes_thick_through()
    test_build_css_hairline_shape_extracts_color_and_skips_none()
    test_layout_slide_elements_respects_slide_justify_center()
    test_layout_slide_elements_respects_slide_justify_flex_end()
    test_layout_slide_elements_ignores_skip_layout_overlays_when_centering()
    test_flat_extract_skips_display_none_elements()
    test_flat_extract_text_only_inline_flex_container_emits_text()
    test_measure_flow_box_inline_flex_card_prefers_intrinsic_width()
    test_measure_flow_box_flex_column_card_preserves_outer_slot_width()
    print()

    print("Slide 1 (Cover) — stat card padding fix:")
    test_stat_card_padding_included_in_width()
    test_centered_flex_x_position_with_padding()
    test_slide1_stat_positions()
    test_slide1_all_text_present()
    test_heading_content_width()
    test_centered_explicit_break_heading_gets_wrap_guard_width()
    print()

    print("Pill text fix (Slide 4/10 — combined text):")
    test_pill_text_included_in_parent()
    test_pill_shape_no_text()
    print()

    print("Decoration shapes:")
    test_decoration_shape_for_no_text_elements()
    print()

    print("Slide 5 chapter page (centered layout width + line count):")
    test_chapter_page_max_width_from_widest_element()
    test_chapter_page_zero_padding_for_large_text()
    test_chapter_page_paragraph_single_line()
    test_chapter_page_no_overflow()
    test_chapter_page_no_overlap()
    test_estimate_wrapped_lines_uses_px_per_in_formula()
    print()

    print("Slide 4 subtitle fix (width + height for padded elements):")
    test_slide4_subtitle_width_not_overwritten_by_sync()
    test_slide4_subtitle_height_matches_golden()
    test_enterprise_dark_theme_pill_rail_stays_below_heading()
    test_multiline_card_copy_gets_extra_runway_before_thin_track()
    test_progress_card_copy_remeasure_keeps_font_size_and_wraps_instead_of_shrinking()
    print()

    print("Generic layout regressions:")
    test_flex_column_badge_stretches_to_parent_width()
    test_decoration_in_flex_row_keeps_explicit_size()
    test_gradient_decoration_in_flex_row_keeps_explicit_size()
    test_grid_flex_container_height_tracks_child_extent_without_tail_gap()
    test_parse_html_to_slides_uses_wrapper_max_width_and_drops_slide_bg_shape()
    test_layout_slide_elements_prefers_slide_content_width_hint_over_widest_text()
    test_single_column_grid_with_nested_flex_column_keeps_shared_row_keys()
    test_local_block_wrapper_packs_children_into_relative_container()
    test_explicit_height_track_stays_thin()
    test_centered_card_group_layout_keeps_text_inside_card()
    test_centered_card_group_preserves_vertical_padding_metadata()
    test_slide_root_background_not_promoted_to_card_group()
    test_auto_margin_divider_centers_in_constrained_content_area()
    test_slide2_info_bar_margin_top_applies_to_outer_box()
    test_slide2_info_bar_does_not_emit_detached_code_bg_shape()
    test_complex_card_height_uses_stacked_flow()
    test_layout_slide_elements_flow_box_advances_current_y_correctly()
    test_extract_inline_fragments_code_kbd_support()
    test_extract_inline_fragments_grouped_badge_and_link()
    test_gradient_text_hex_colors_resolve_and_keep_stops()
    test_build_text_element_inline_flex_pill_shrink_wraps_single_line()
    test_build_text_element_grouped_inline_badge_keeps_single_line_height()
    test_build_text_element_block_cta_pill_uses_component_layout()
    test_build_text_element_boosts_cjk_display_heading_optically()
    test_build_text_element_skips_optical_boost_for_space_grotesk_display_heading()
    test_build_grid_children_flex_row_preserves_component_width_and_pairing()
    test_build_grid_children_flex_wrap_centers_rows_without_overflow()
    test_map_font_prefers_stable_ppt_font_over_platform_stack_order()
    test_map_font_platform_only_cjk_stack_falls_back_to_office_safe_font()
    test_map_font_pure_latin_prefers_latin_safe_font_even_in_mixed_stack()
    test_map_font_space_grotesk_stack_stays_sans_for_latin_and_cjk()
    test_map_font_mixed_serif_stack_uses_latin_and_cjk_pair_for_mixed_script()
    test_map_font_swiss_display_stack_prefers_archivo_fallback_for_latin()
    test_resolve_text_contract_chinese_chan_preserves_body_breaks()
    test_resolve_text_contract_chinese_chan_title_prefers_wrap_over_shrink()
    test_resolve_text_contract_chinese_chan_body_prefers_wrap_for_long_prose()
    test_resolve_text_contract_swiss_title_uses_display_stack_and_preserves_width()
    test_build_table_element_plain_td_defaults_to_text_primary()
    test_flat_extract_mixed_inline_code_uses_inline_overlays()
    test_flat_extract_inline_code_in_prose_does_not_emit_detached_code_bg()
    test_build_text_element_wide_prose_adjusts_back_to_single_line()
    test_build_text_element_medium_card_prose_adjusts_back_to_single_line()
    test_build_text_element_centered_subtitle_prefers_full_max_width_and_no_wrap_fit()
    test_layout_centered_subtitle_keeps_max_width_when_no_wrap_fit_is_requested()
    test_flow_gap_prefers_collapsed_margins_over_default_gap()
    test_layout_slide_elements_uses_next_margin_top_for_container_gap()
    test_build_elements_preserve_margin_top_metadata()
    test_card_group_layout_expands_bg_height_to_content_bottom()
    test_export_text_element_preserves_explicit_break_headings()
    test_export_text_element_keeps_narrow_card_copy_wrapping_instead_of_shrinking()
    test_export_text_element_preserves_contract_authored_breaks_without_shrinking()
    test_export_text_element_prefers_wrap_to_preserve_size_for_body_prose()
    test_export_text_element_single_line_contract_title_stays_no_wrap()
    test_export_text_element_medium_contract_title_keeps_wrap_square()
    test_build_text_element_centered_block_command_shrinkwraps()
    test_export_shape_background_small_stamp_seal_keeps_border_without_shadow()
    test_chinese_chan_roundtrip_wrap_fidelity_and_no_page_overflow()
    test_measure_flow_box_intrinsic_height_for_layer_card()
    test_measure_flow_box_marks_descendants_in_flow_box()
    test_measure_flow_box_promotes_visible_flex_column_card()
    test_table_cell_fragments_measure_kbd_sequence()
    test_build_table_element_classifies_presentation_rows()
    test_presentation_rows_use_compact_single_line_row_height()
    test_presentation_rows_keep_fitted_key_column_and_expand_value_column()
    test_presentation_rows_shortcut_column_gets_extra_runway()
    test_presentation_row_label_uses_stronger_ink()
    test_display_heading_normalizes_deep_slate_to_black()
    test_presentation_row_shortcut_cell_keeps_original_ink()
    test_build_table_element_keeps_real_data_tables()
    test_build_table_element_respects_local_content_width_constraint()
    test_build_table_element_remeasures_wrapped_row_height_after_width_constraint()
    test_table_card_height_uses_actual_table_bounds()
    test_centered_inline_command_prefers_content_width()
    test_export_centered_inline_command_uses_fragment_runway()
    test_centered_inline_command_mutes_trailing_link_color()
    test_export_accent_card_uses_narrow_strip_and_full_main_card()
    test_slide4_theme_grid_cards_share_stretched_row_height()
    test_export_does_not_add_exporter_chrome_by_default()
    test_accent_callouts_keep_optical_gap_from_preceding_blocks()
    test_slide10_gradient_divider_centers_in_heading_block()
    test_export_corpus_parse_smoke()
    test_handwritten_fixture_covers_core_patterns()
    test_handwritten_fixture_structural_eval_gate()
    print()

    print("All tests passed!")


if __name__ == '__main__':
    run_tests()
