# Deployment Patterns

Use this reference when the bot must be packaged or deployed.

## Minimum Deploy Checklist

- environment variables supplied securely
- production start command defined
- logs visible in the runtime environment
- command registration plan documented
- privileged intents enabled in the developer portal if required
- persistent storage path or database connection configured

## Docker Guidance

Use Docker when:
- deployment target supports containers
- environment parity matters
- the project already uses containers

Keep images simple:
- install only runtime dependencies in final image
- copy only necessary files
- avoid baking secrets into the image

## Process Management

For VPS deployment, common options:
- Docker compose
- systemd service
- PM2 for Node.js when lightweight process supervision is acceptable

## Operational Safety

- restart on failure
- write structured logs if possible
- avoid features that require local writable disk unless the host guarantees persistence
