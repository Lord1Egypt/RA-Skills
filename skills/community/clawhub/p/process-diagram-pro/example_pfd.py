# -*- coding: utf-8 -*-
"""
Example: Generate PFD (Process Flow Diagram)
============================================

Usage:
    cd /path/to/process-diagram-pro
    python3 example_pfd.py

Output:
    example_pfd.png
"""

import sys
sys.path.insert(0, '.')

from chem_diagram_v3 import PFDGenerator

# Create PFD generator
gen = PFDGenerator()

# Set title
gen.set_title("Maleic Anhydride Hydrogenation", "PFD")

# Add equipment
gen.add_equipment({
    'type': 'tank',
    'x': 1, 'y': 3,
    'tag': 'T-101',
    'name': 'MA Tank',
    'note': 'T: RT~60°C'
})

gen.add_equipment({
    'type': 'reactor',
    'x': 5, 'y': 3,
    'tag': 'R-01',
    'name': 'Fixed Bed Reactor',
    'temp': 140,
    'pressure': 4.0,
    'catalyst': '3%Pd/C'
})

gen.add_equipment({
    'type': 'separator',
    'x': 8, 'y': 3,
    'tag': 'V-01',
    'name': 'Gas-Liquid Separator'
})

# Add material flows
gen.add_flow({
    'from': 'T-101',
    'to': 'R-01',
    'label': 'MA + H₂',
    'temp': 60
})

gen.add_flow({
    'from': 'R-01',
    'to': 'V-01',
    'label': 'Product',
    'temp': 140
})

# Save
gen.save('example_pfd.png')
print("✅ PFD generated: example_pfd.png")
