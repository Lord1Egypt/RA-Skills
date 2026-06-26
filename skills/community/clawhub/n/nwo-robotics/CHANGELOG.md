# Changelog

## [1.0.2] - 2025-03-19

### Fixed
- Updated homepage to https://nworobotics.cloud
- Updated repository to https://huggingface.co/spaces/PUBLICAE/nwo-robotics-api-demo

## [1.0.1] - 2025-03-19

### Fixed
- Added `homepage` field to skill.yaml for ClawHub registry
- Added `repository` field to skill.yaml
- Added `required_env_vars` list for registry metadata clarity
- Updated SKILL.md with homepage and repository links

## [1.0.0] - 2025-03-19

### Added
- Initial release of NWO Robotics OpenClaw Skill
- Robot control via natural language
- IoT sensor querying
- Vision-based object detection
- Voice and gesture command support
- Task planning and orchestration
- Emergency stop functionality
- Input validation and sanitization
- Rate limit awareness
- User-provided API key security model

### Security
- No embedded API credentials
- Command allowlist validation
- Input length limits
- HTML/script injection prevention
- Secure header handling

### Documentation
- Comprehensive SKILL.md
- README with quick start guide
- Example commands documentation
- MIT-0 license included
