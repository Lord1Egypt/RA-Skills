# CP2K Job Report

## User request summary

The user asked for a CP2K job to be generated from a simple natural-language description and an uploaded structure file.

## Interpreted job type

- Task type: {{ task_type }}
- System type: {{ system_type }}
- Structure file: {{ structure_file }}
- Periodicity: {{ periodicity }}
- Charge: {{ charge }}
- Multiplicity: {{ multiplicity }}
- Priority: {{ priority }}

## Hardware information

- Hardware type: {{ hardware.type }}
- CPU/GPU cores: {{ hardware.cores }}
- Memory (GB): {{ hardware.memory_gb }}

## Defaults applied

{% if defaults_applied %}
{% for item in defaults_applied %}
- {{ item }}
{% endfor %}
{% else %}
- No automatic defaults were recorded.
{% endif %}

## Notes and warnings

{% if notes %}
{% for item in notes %}
- {{ item }}
{% endfor %}
{% else %}
- No additional warnings.
{% endif %}

## CP2K drafting summary

The generated CP2K input draft is intended as a practical starting point rather than a guaranteed optimal setup.

For the current first-version workflow, the draft typically assumes:
- a Quickstep DFT-style setup
- explicit coordinates for simple systems
- a conservative molecular treatment for xyz-only isolated structures
- a vacuum box for non-periodic molecular calculations when needed

## User review checklist

Before running the job, review the following:

- Is the task type correct?
- Is the system really molecular / crystal / surface as inferred?
- Are charge and multiplicity correct?
- Is the periodicity correct?
- Is the chosen priority (fast / balanced / high) appropriate?
- For xyz-only molecular jobs, is the automatically chosen vacuum box acceptable?
- For production calculations, have cutoff / basis / method settings been convergence-tested?

## Scope note

This generated input is a first-pass draft.  
It is designed to reduce manual setup effort, not to replace expert validation for difficult systems.