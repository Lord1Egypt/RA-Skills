# -*- coding: utf-8 -*-
"""
Process Diagram Pro v3.0
=========================

Professional PFD/P&ID Diagram Generator for Chemical Process Industries

Core Modules:
    - ChemicalCanvas: Main canvas for drawing
    - Devices: Tank, Reactor, HeatExchanger, Separator, Valve, Instrument
    - Pipelines: Pipe, FlowArrow, SignalLine, Components
    - Diagrams: PFD, P&ID, SystemArchitecture

Usage:
    from chem_diagram_v3 import ChemicalCanvas, PFDGenerator, PIDGenerator
    
    canvas = ChemicalCanvas(figsize=(16, 8))
    canvas.add_device(...)
    canvas.add_pipe(...)
    canvas.save('output.png')
"""

__version__ = '3.0.0'
__author__ = 'Process Diagram Pro Team'

from .core.canvas import ChemicalCanvas
from .core.colors import COLORS, TEMP_COLORS
from .devices.base import Device
from .devices.tanks import Tank
from .devices.reactors import Reactor
from .devices.heat_exchangers import HeatExchanger
from .devices.separators import Separator
from .devices.valves import ControlValve, ESDValve, SafetyValve
from .devices.instruments import Instrument
from .pipelines.pipe import Pipe
from .diagrams.pfd import PFDGenerator
from .diagrams.pid import PIDGenerator
from .diagrams.architecture import ArchitectureGenerator

__all__ = [
    'ChemicalCanvas',
    'Device',
    'Tank',
    'Reactor', 
    'HeatExchanger',
    'Separator',
    'ControlValve',
    'ESDValve',
    'SafetyValve',
    'Instrument',
    'Pipe',
    'PFDGenerator',
    'PIDGenerator',
    'ArchitectureGenerator',
    'COLORS',
    'TEMP_COLORS',
]
