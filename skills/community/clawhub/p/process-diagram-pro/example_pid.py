# -*- coding: utf-8 -*-
"""
Example: Generate P&ID (Piping & Instrumentation Diagram)
==========================================================

Usage:
    cd /path/to/process-diagram-pro
    python3 example_pid.py

Output:
    example_pid.png
"""

import sys
sys.path.insert(0, '.')

from chem_diagram_v3 import PIDGenerator

# Create P&ID generator
gen = PIDGenerator()

# Set title
gen.set_title("Maleic Anhydride Hydrogenation", "P&ID with Control Loops & ESD")

# Add equipment
gen.add_equipment({
    'type': 'tank', 'x': 1, 'y': 3,
    'tag': 'T-101', 'name': 'MA Tank'
})

gen.add_equipment({
    'type': 'reactor', 'x': 6, 'y': 3,
    'tag': 'R-01', 'name': 'Fixed Bed Reactor', 
    'temp': 140, 'pressure': 4.0
})

gen.add_equipment({
    'type': 'separator', 'x': 10, 'y': 3,
    'tag': 'V-01', 'name': 'Separator'
})

# Add valves
gen.add_valve({'type': 'esd', 'x': 3, 'y': 3, 'tag': 'XV-101'})
gen.add_valve({'type': 'control', 'x': 4.5, 'y': 3, 'tag': 'TV-101'})
gen.add_valve({'type': 'esd', 'x': 8, 'y': 3, 'tag': 'XV-102'})

# Add instruments
gen.add_instrument({'type': 'TIC', 'x': 6, 'y': 5, 'tag': 'TIC-101'})
gen.add_instrument({'type': 'PIC', 'x': 8, 'y': 5, 'tag': 'PIC-101'})
gen.add_instrument({'type': 'TE', 'x': 5.5, 'y': 2, 'tag': 'TE-101'})
gen.add_instrument({'type': 'PE', 'x': 7.5, 'y': 2, 'tag': 'PE-101'})

# Add signal lines (gray dashed lines)
gen.add_signal({'from': 'TE-101', 'to': 'TIC-101'})
gen.add_signal({'from': 'PE-101', 'to': 'PIC-101'})

# Add ESD box
gen.add_esd_box(0.5, 1, ['T>170°C', 'P>5.5MPa', 'H₂ Leak'])

# Save
gen.save('example_pid.png')
print("✅ P&ID generated: example_pid.png")
