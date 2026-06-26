#!/bin/bash
# Fullstack App Generator

set -e

NAME="${1:-my-app}"
FRONTEND="${2:-react}"
BACKEND="${3:-node}"
DB="${4:-postgresql}"

echo "🚀 Generating fullstack app: $NAME"
echo "📦 Frontend: $FRONTEND | Backend: $BACKEND | DB: $DB"

# Create directory
mkdir -p "$NAME"
cd "$NAME"

# Create frontend
case $FRONTEND in
  react)
    mkdir -p frontend
    cat > frontend/package.json << EOF
{
  "name": "$NAME-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
EOF
    ;;
  vue)
    mkdir -p frontend
    cat > frontend/package.json << EOF
{
  "name": "$NAME-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build"
  },
  "dependencies": {
    "vue": "^3.3.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
EOF
    ;;
  next)
    mkdir -p frontend
    cat > frontend/package.json << EOF
{
  "name": "$NAME-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
EOF
    ;;
esac

# Create backend
mkdir -p backend
case $BACKEND in
  node)
    cat > backend/package.json << EOF
{
  "name": "$NAME-backend",
  "version": "1.0.0",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5"
  }
}
EOF
    mkdir -p backend/src
    cat > backend/src/index.js << EOF
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(\`Server running on port \${PORT}\`));
EOF
    ;;
  python)
    cat > backend/requirements.txt << EOF
fastapi==0.104.0
uvicorn==0.24.0
sqlalchemy==2.0.0
EOF
    mkdir -p backend/app
    cat > backend/app/main.py << EOF
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
    ;;
esac

# Create docker-compose
cat > docker-compose.yml << EOF
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "${BACKEND:-$((3000+1))}"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/$NAME

  db:
    image: $DB
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: $NAME
EOF

echo "✅ Generated $NAME fullstack app!"
echo "📝 Next steps:"
echo "   cd $NAME"
echo "   docker-compose up"
