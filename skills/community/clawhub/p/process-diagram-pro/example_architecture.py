# -*- coding: utf-8 -*-
"""
Example: Generate System Architecture Diagram
=============================================

Usage:
    cd /path/to/process-diagram-pro
    python3 example_architecture.py

Output:
    example_architecture.png
"""

import sys
sys.path.insert(0, '.')

from chem_diagram_v3 import ArchitectureGenerator

# Create architecture generator
gen = ArchitectureGenerator()

# Set title
gen.set_title("Digital Twin System Architecture", "Chemical Plant")

# Add layers
gen.add_layer("Device Layer", [
    "Temp Sensor", "Pressure Sensor",
    "Flow Meter", "PLC Controller"
])

gen.add_layer("Edge Computing", [
    "ESP32 Gateway", "Edge Agent",
    "Local Data Cache"
])

gen.add_layer("Cloud Platform", [
    "MQTT Broker", "Time Series DB",
    "AI Inference", "Digital Twin Engine"
])

gen.add_layer("Application Layer", [
    "HMI Dashboard", "Alarm System",
    "Data看板", "Mobile App"
])

# Save
gen.save('example_architecture.png')
print("✅ Architecture diagram generated: example_architecture.png")
