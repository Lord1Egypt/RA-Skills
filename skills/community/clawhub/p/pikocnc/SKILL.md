# PikoCNC G-Code Full Skill (Complete Implementation-Oriented)

## PURPOSE
This document represents a **complete, implementation-oriented skill** for PikoCNC G-code.
It includes:
- Full command coverage (based on manual)
- Modal state model
- Execution rules
- Examples per command
- Interpreter-ready structure

---

# 1. MACHINE STATE MODEL

## Modal Groups
- Motion: G0, G1, G2, G3
- Units: G20, G21
- Cycle: G80, G81
- Scaling: G51

## State Variables
- Position: X, Y, Z
- Feed rate: F
- Spindle: S
- Motion mode
- Unit mode
- Active cycle
- Scaling factor
- Tool number

---

# 2. PROGRAM STRUCTURE

## Start / End
%
...
M30

## Comments
( comment )
; comment
' comment

---

# 3. CORE COMMANDS

## G0 – Rapid
G0 X10 Y10

## G1 – Linear
G1 X20 Y20 F100

## G2 – CW Arc
G2 X20 Y20 I5 J0

## G3 – CCW Arc
G3 X20 Y20 I-5 J0

### Rules
- I/J relative to start point
- R optional (alternative)
- Do not mix I/J with R

---

# 4. UNITS

## G20 – Inches
G20

## G21 – Millimeters
G21

---

# 5. DWELL

## G4
G4 P2

---

# 6. HOMING

## G28
G28

## G30
G30

---

# 7. DRILLING

## G81
G98
G81 X10 Y10 Z-5 R2 F100

## Cancel
G80

---

# 8. SCALING

## G51
G51 I1.5
G51 I1.5 X10 Y10

---

# 9. PARAMETERS

F100
S1000

---

# 10. M-CODES

M0
M3 S1000
M4
M5
M6 T1
M8
M9
M10
M11
M30

---

# 11. TOOL CHANGE EXECUTION

M6 triggers:
1. M6_beg
2. M6_put
3. M6_get
4. M6_mess
5. M6_end

---

# 12. MODAL RULES

- Motion persists
- Feed persists
- Units persist

Example:
G1 X10 Y10
X20 Y20

---

# 13. NON-MODAL

- I
- J
- R

---

# 14. EXECUTION ENGINE (INTERPRETER LOGIC)

## Step Processing
1. Parse line
2. Update modal state
3. Execute motion
4. Apply parameters

## Motion Execution
- G0: instant move
- G1: linear interpolation
- G2/G3: arc interpolation

---

# 15. ERROR HANDLING

- Missing parameters → error
- Invalid arc definition → error
- Unknown command → ignore or error

---

# 16. SAFE PROGRAM TEMPLATE

%
G21
G0 Z5
G0 X0 Y0
G1 Z-1 F100
G1 X50 Y0
G1 X50 Y50
G1 X0 Y50
G1 X0 Y0
G0 Z5
M30

---

# 17. BEST PRACTICES

- Always set units
- Always retract Z before rapid XY
- Avoid mixing arc definitions
- Reset states when needed

---

# 18. IMPLEMENTATION NOTES

To build interpreter in C#:
- Lexer → tokenize line
- Parser → command objects
- State machine → modal tracking
- Executor → motion simulation

---

# SUMMARY

This file provides:
- Full command coverage
- Execution semantics
- Interpreter-ready structure

It can be used for:
- CNC programming
- G-code validation
- Simulator development
