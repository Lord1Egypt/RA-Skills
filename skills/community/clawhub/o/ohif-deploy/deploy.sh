#!/bin/bash
# OHIF Deployment Script

set -e

PORT="${1:-3000}"
DATA_SOURCE="${2:-tbidea}"

echo "🚀 Deploying OHIF Medical Imaging Viewer..."
echo "📦 Port: $PORT"
echo "🔗 Data Source: $DATA_SOURCE"

# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  ohif:
    image: ohif/viewer:latest
    ports:
      - "${PORT}:3000"
    environment:
      - APP_CONFIG=/usr/local/share/ohif/static/hosting.json
    volumes:
      - ./config:/usr/local/share/ohif/static
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - ohif
    restart: unless-stopped
EOF

# Create config
mkdir -p config
cat > config/hosting.json << EOF
{
  "defaultDataSourceName": "${DATA_SOURCE}",
  "dataSources": [
    {
      "namespace": "@ohif/extension-default.dataSourcesModule.dicomweb",
      "sourceName": "${DATA_SOURCE}",
      "configuration": {
        "wadoUriRoot": "https://www.allhealthai.com/HealthRecordCenter",
        "qidoRoot": "https://www.allhealthai.com/HealthRecordCenter",
        "wadoRoot": "https://scnc.allhealthai.com:16010/HealthRecordCenter",
        "imageRendering": "wadors",
        "thumbnailRendering": "wadors",
        "enableStudyLazyLoad": true
      }
    }
  ]
}
EOF

echo "✅ Configuration created!"
echo "🚀 Run: docker-compose up -d"
