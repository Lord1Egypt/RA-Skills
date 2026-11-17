"""交互面板结构测试。

验证意图：神经元治理必须发生在认知画布内，避免用户在光点与页面下方详情区之间
来回寻找；其余治理视图必须复用同一套视觉语义。
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memoryguard.interactive import render_interactive_html  # noqa: E402


def test_neuron_governance_is_an_in_canvas_popover() -> None:
    html = render_interactive_html()

    stage = html.index('id="neuron-stage"')
    popover = html.index('id="neuron-popover"')

    assert stage < popover
    assert 'id="neuron-detail"' not in html
    assert "positionNeuronPopover" in html
    assert "确认这组记忆" in html
    assert "解除这组关联" in html


def test_all_views_share_the_neural_visual_system() -> None:
    html = render_interactive_html()

    assert "--accent: #6ee7c4" in html
    assert 'class="brand-orb"' in html
    assert 'class="health-ring"' in html
    assert 'class="finding-item' in html
    assert 'class="plan-item' in html
    assert 'class="neuron-shell"' in html
