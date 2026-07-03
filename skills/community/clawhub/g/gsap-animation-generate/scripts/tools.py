from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def understand_and_create_animation(
    request: str,
    context: Optional[str] = "react",
    complexity: Optional[str] = "intermediate"
) -> Dict[str, Any]:
    """
    The main AI engine - understands any animation request and generates perfect GSAP code with surgical precision
    
    Args:
        request: Natural language description of the animation you want (e.g., "fade in cards one by one when scrolling", "create a hero entrance with staggered text")
        context: Development context and requirements
        complexity: Animation complexity level
    
    Returns:
        
    """
    arguments = {
        "request": request,
        "context": context,
        "complexity": complexity
    }
    
    return call_api("1777316659553283", "understand_and_create_animation", arguments)

def get_gsap_api_expert(
    api_element: str,
    level: Optional[str] = "advanced"
) -> Dict[str, Any]:
    """
    Deep dive into any GSAP method, plugin, or property with expert-level knowledge
    
    Args:
        api_element: GSAP API element (e.g., "gsap.to", "ScrollTrigger", "SplitText", "drawSVG", "morphSVG")
        level: Detail level needed
    
    Returns:
        
    """
    arguments = {
        "api_element": api_element,
        "level": level
    }
    
    return call_api("1777316659553283", "get_gsap_api_expert", arguments)

def generate_complete_setup(
    framework: str,
    plugins: Optional[null] = None,
    performance_level: Optional[str] = "optimized"
) -> Dict[str, Any]:
    """
    Generate complete GSAP environment setup with all plugins and optimizations
    
    Args:
        framework: Target framework
        plugins: Specific plugins needed
        performance_level: Performance optimization level
    
    Returns:
        
    """
    arguments = {
        "framework": framework,
        "plugins": plugins,
        "performance_level": performance_level
    }
    
    return call_api("1777316659553283", "generate_complete_setup", arguments)

def debug_animation_issue(
    issue: str,
    code: Optional[str] = None,
    expected_behavior: Optional[str] = None
) -> Dict[str, Any]:
    """
    Expert debugging for GSAP animation problems with solutions
    
    Args:
        issue: Description of the animation problem or unexpected behavior
        code: Problematic animation code (optional but helpful)
        expected_behavior: What should happen vs what is happening
    
    Returns:
        
    """
    arguments = {
        "issue": issue,
        "code": code,
        "expected_behavior": expected_behavior
    }
    
    return call_api("1777316659553283", "debug_animation_issue", arguments)

def optimize_for_performance(
    animation_code: str,
    target: Optional[str] = "60fps-desktop"
) -> Dict[str, Any]:
    """
    Transform any animation into 60fps smoothness with expert optimizations
    
    Args:
        animation_code: Existing GSAP animation code to optimize
        target: Optimization target
    
    Returns:
        
    """
    arguments = {
        "animation_code": animation_code,
        "target": target
    }
    
    return call_api("1777316659553283", "optimize_for_performance", arguments)

def create_production_pattern(
    pattern_type: str,
    industry: Optional[str] = "portfolio"
) -> Dict[str, Any]:
    """
    Generate battle-tested, production-ready animation patterns
    
    Args:
        pattern_type: Type of production pattern needed
        industry: Industry or use case
    
    Returns:
        
    """
    arguments = {
        "pattern_type": pattern_type,
        "industry": industry
    }
    
    return call_api("1777316659553283", "create_production_pattern", arguments)

