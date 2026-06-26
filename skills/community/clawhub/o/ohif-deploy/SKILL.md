# OHIF Medical Imaging Viewer Deployment

Deploy OHIF (Open Health Imaging Foundation) viewer with Docker.

## Features

- One-click Docker deployment
- DICOMweb data source configuration
- Custom DICOM server integration
- Support for tbidea, orthanc, DCM4CHEE
- SSL/TLS configuration
- Production-ready setup

## Usage

```bash
# Deploy with default settings
./deploy.sh

# Deploy with custom config
./deploy.sh --datasource tbidea --port 3000

# Deploy with SSL
./deploy.sh --ssl --domain your-domain.com
```

## Configuration

Supports multiple DICOMweb servers:
- tbidea (default)
- orthanc
- DCM4CHEE
- AWS S3

## Requirements

- Docker
- Docker Compose
- 2GB RAM minimum

## Author

Sunshine-del-ux
