## Description:

Late Brake is a CLI racing lap analysis skill that imports NMEA and RaceChrono VBO telemetry, splits laps automatically, compares laps, and returns structured results for AI coaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isaachan](https://clawhub.ai/user/isaachan)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers, racing coaches, and developers use Late Brake to parse racing telemetry, split sessions into laps, and compare complete laps by lap time, sector, corner, and speed metrics for coaching or batch analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cache files are written next to telemetry inputs, and unsafe shared or attacker-writable directories could expose users to accidental overwrites.

Mitigation: Run the skill on telemetry stored in trusted private directories, avoid shared or attacker-writable paths, and review or remove generated cache files when handling sensitive data.

Risk: Custom track data is stored under ~/.late-brake/tracks and can update an existing custom track with the same ID.

Mitigation: Review custom track JSON and track IDs before adding them, and keep the user track directory access-controlled and backed up.

## Reference(s):

- [Compare JSON Schema](references/compare-json-schema.md)
- [Internal Data Format](references/data-format.md)
- [Track Data Format](references/track-format.md)
- [VBO Format Specification](references/vbo-format.md)
- [Distance from a point to a line on a sphere](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#On_a_sphere)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [CLI text tables or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comparison JSON includes lap, sector, corner, speed, distance, and time-difference fields; parsed laps may be cached locally.]

## Skill Version(s):

0.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
