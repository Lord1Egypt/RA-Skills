from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_diagram_doc(
    diagram_name: null
) -> Dict[str, Any]:
    """
    
Retrieve the documentation content for a specific Mermaid diagram.

Args:
    diagram_name (DiagramType): The name of the diagram. Possible values are: 'architecture', 'block', 'c4', 'classDiagram', 'entityRelationshipDiagram', 'examples', 'flowchart', 'gantt', 'gitgraph', 'kanban', 'mindmap', 'packet', 'pie', 'quadrantChart', 'radar', 'requirementDiagram', 'sankey', 'sequenceDiagram', 'stateDiagram', 'timeline', 'userJourney', 'xyChart', 'zenuml'. These are case sensitive strings.

Returns:
    str: The documentation content as a string, or an empty string if the diagram is not found.

    
    Args:
        diagram_name: null
    
    Returns:
        null
    """
    arguments = {
        "diagram_name": diagram_name
    }
    
    return call_api("1777419067505667", "get_diagram_doc", arguments)

