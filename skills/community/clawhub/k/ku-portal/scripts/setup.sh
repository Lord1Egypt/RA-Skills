#!/usr/bin/env bash
# ku-portal 스킬 자동 설치 스크립트
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$SKILL_DIR/.venv"
PKG="ku-portal-mcp"

echo "📦 ku-portal 스킬 설치"
echo "  스킬 경로: $SKILL_DIR"

# 1) venv 생성
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 가상환경 생성 중..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ 가상환경 이미 존재"
fi

# 2) pip 업그레이드 + 패키지 설치
echo "📥 $PKG 설치/업데이트 중..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install --upgrade "$PKG" -q

# 3) 버전 확인
VERSION=$("$VENV_DIR/bin/python3" -c "import ku_portal_mcp; print(ku_portal_mcp.__version__)" 2>/dev/null || echo "unknown")
echo "✅ $PKG $VERSION 설치 완료"

# 4) 자격 증명 안내
CREDS="$HOME/.config/ku-portal/credentials.json"
if [ ! -f "$CREDS" ]; then
    echo ""
    echo "⚠️  KUPID 자격 증명 파일이 없습니다."
    echo "  도서관/메뉴 조회는 바로 가능하지만, 로그인 필요 기능은 아래 파일을 먼저 만들어주세요:"
    echo ""
    echo "  mkdir -p ~/.config/ku-portal"
    echo '  echo '\''{"id": "학번", "pw": "비밀번호"}'\'' > ~/.config/ku-portal/credentials.json'
    echo "  chmod 600 ~/.config/ku-portal/credentials.json"
else
    echo "✅ 자격 증명 파일 확인됨"
fi

echo ""
echo "🎉 설치 완료. 사용법:"
echo "  source $VENV_DIR/bin/activate"
echo "  python3 $SKILL_DIR/ku_query.py library"
