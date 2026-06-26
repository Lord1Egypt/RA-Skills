# Microservices Starter

Build production-ready microservices architecture.

## Features

### API Gateway
- Request routing
- Rate limiting
- Authentication
- Load balancing

### Service Templates
- Node.js microservice
- Python microservice
- Go microservice

### Service Mesh Ready
- Kubernetes manifests
- Istio configurations
- Prometheus metrics

### Distributed Tracing
- OpenTelemetry integration
- Jaeger support
- Request tracing

### Container Orchestration
- Docker Compose
- Kubernetes manifests
- Helm charts

## Quick Start

```bash
# Create new service
./create-service.sh user-service --lang node

# Create API gateway
./create-gateway.sh

# Deploy to K8s
./deploy.sh production

# Add monitoring
./monitor.sh install
```

## Architecture

```
┌─────────────┐
│   Gateway   │
└──────┬──────┘
       │
┌──────┴──────┐
│  Services   │
└──────┬──────┘
       │
┌──────┴──────┐
│  Database   │
└─────────────┘
```

## Services Included

- User Service
- Order Service
- Product Service
- Payment Service
- Notification Service

## Requirements

- Docker 20.10+
- Kubernetes 1.24+
- Helm 3.8+

## Author

Sunshine-del-ux
