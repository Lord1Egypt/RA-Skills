#!/bin/sh
# Installe Memoria sur un Mac neuf (ex. l'iMac de Luna) — pensé pour un non-dev.
# Une seule commande :
#   curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/memoria-v1/scripts/install-memoria.sh | sh
# ou, dépôt déjà cloné :  sh scripts/install-memoria.sh
#
# Fait : vérifie git + Node, clone/maj le dépôt, installe, construit, démarre le
# daemon, configure le PATH, active le lancement au login (macOS) et OUVRE
# l'interface web. Idempotent (relançable sans risque sur une machine propre).
#
# Variables d'environnement (défauts sensés — utiles surtout pour les tests) :
#   MEMORIA_REPO_DIR  dossier du dépôt        (défaut $HOME/openclaw-memoria)
#   MEMORIA_HOME      dossier de données      (défaut $HOME/.memoria/data)
#   MEMORIA_BIN_DIR   dossier du raccourci    (défaut $HOME/.local/bin)
#   MEMORIA_ZSHRC     fichier de profil shell (défaut $HOME/.zshrc)
set -eu

REPO_URL="${MEMORIA_REPO_URL:-https://github.com/Primo-Studio/openclaw-memoria.git}"
BRANCH="${MEMORIA_BRANCH:-memoria-v1}"
# MEMORIA_HOME_REPO = ancien nom, accepté pour compatibilité.
DEST="${MEMORIA_REPO_DIR:-${MEMORIA_HOME_REPO:-$HOME/openclaw-memoria}}"
BIN_DIR="${MEMORIA_BIN_DIR:-$HOME/.local/bin}"
DATA="${MEMORIA_HOME:-$HOME/.memoria/data}"
ZSHRC="${MEMORIA_ZSHRC:-$HOME/.zshrc}"
OS="$(uname -s)"

say()  { printf '\033[1;36m▸ %s\033[0m\n' "$1"; }
warn() { printf '\033[1;33m⚠ %s\033[0m\n' "$1"; }
err()  { printf '\033[1;31m✗ %s\033[0m\n' "$1" >&2; exit 1; }

# 0) Outils de développement (git). Sur macOS ils arrivent avec les
#    Command Line Tools d'Apple — on déclenche le popup système si absents.
if [ "$OS" = "Darwin" ]; then
  if ! xcode-select -p >/dev/null 2>&1; then
    say "Memoria a besoin des outils de développement Apple (gratuits, ~5 min)."
    say "Une fenêtre système va s’ouvrir : clique sur « Installer » et attends la fin."
    xcode-select --install || true # déjà en cours d'installation = pas une erreur
    printf '\n\033[1;36m▸ Quand l’installation est terminée, RELANCE simplement ce script (même commande).\033[0m\n\n'
    exit 0
  fi
else
  command -v git >/dev/null 2>&1 || err "git manquant. Installe-le (ex. sudo apt install git) puis relance ce script."
fi
say "Outils de développement OK"

# 1) Node >= 20 (22 LTS recommandé pour cohabiter avec OpenClaw)
command -v node >/dev/null 2>&1 || err "Node.js manquant. Installe Node 22 LTS depuis https://nodejs.org puis relance."
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
[ "$NODE_MAJOR" -ge 20 ] || err "Node $NODE_MAJOR détecté ; Memoria requiert Node 20+ (22 LTS conseillé)."
if [ $((NODE_MAJOR % 2)) -ne 0 ]; then
  warn "Node $(node -v) est une version non-LTS (numéro impair). Recommandé : Node 22 LTS depuis https://nodejs.org. On continue quand même."
fi
say "Node $(node -v) OK"

# 2) cloner ou mettre à jour — avec GARDE ANTI-ÉCRASEMENT : si le dépôt local
#    contient des modifications, on REFUSE de faire un reset --hard dessus
#    (protège une machine de développement d'une relance accidentelle).
if [ -d "$DEST/.git" ]; then
  if [ -n "$(git -C "$DEST" status --porcelain)" ]; then
    err "Des modifications locales existent dans $DEST — ce script est réservé aux installations propres. Utilise plutôt : memoria update"
  fi
  say "Mise à jour du dépôt dans $DEST"
  git -C "$DEST" fetch --depth 1 origin "$BRANCH"
  git -C "$DEST" checkout "$BRANCH"
  git -C "$DEST" reset --hard "origin/$BRANCH"
else
  say "Clonage de Memoria dans $DEST"
  git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$DEST"
fi

# 3) installer + construire
say "Installation des dépendances (peut prendre 1-2 min)…"
npm --prefix "$DEST" install --no-audit --no-fund
say "Construction…"
npm --prefix "$DEST" run build

# 4) raccourci CLI 'memoria' dans ~/.local/bin — node est résolu AU RUNTIME
#    (command -v node), avec repli sur le chemin figé au moment de l'install
#    (si le PATH du shell de login diffère, ex. lancement par double-clic).
mkdir -p "$BIN_DIR"
NODE_AT_INSTALL="$(command -v node)"
cat > "$BIN_DIR/memoria" <<EOF
#!/bin/sh
# Raccourci Memoria (généré par install-memoria.sh).
MEMORIA_NODE_FALLBACK="$NODE_AT_INSTALL"
NODE_BIN="\$(command -v node 2>/dev/null || true)"
[ -n "\$NODE_BIN" ] || NODE_BIN="\$MEMORIA_NODE_FALLBACK"
exec "\$NODE_BIN" "$DEST/packages/cli/dist/bin.js" "\$@"
EOF
chmod +x "$BIN_DIR/memoria"

# 5) init + démarrage du daemon. `memoria init` est idempotent (config déjà en
#    place = « ✓ config existante », code 0) : toute VRAIE erreur s'affiche et
#    arrête le script — on n'avale plus sa sortie.
say "Initialisation du stockage…"
"$BIN_DIR/memoria" init
say "Démarrage du service…"
"$BIN_DIR/memoria" start

# 6) PATH dans le profil shell — bloc marqué, ajouté UNE seule fois.
if [ ! -f "$ZSHRC" ] || ! grep -q '# >>> memoria >>>' "$ZSHRC"; then
  {
    printf '\n# >>> memoria >>>\n'
    printf 'export PATH="%s:$PATH"\n' "$BIN_DIR"
    printf '# <<< memoria <<<\n'
  } >>"$ZSHRC"
  say "Commande « memoria » ajoutée au PATH ($ZSHRC)"
else
  say "PATH déjà configuré ($ZSHRC)"
fi
case ":$PATH:" in
  *":$BIN_DIR:"*) : ;;
  *) PATH="$BIN_DIR:$PATH" ;; # pour la suite de CE script
esac

# 7) lancement automatique au login (launchd — macOS uniquement pour l'instant)
if [ "$OS" = "Darwin" ]; then
  say "Activation du lancement automatique au démarrage…"
  "$BIN_DIR/memoria" autostart on
else
  warn "Lancement auto au login : macOS uniquement pour l’instant. Après un redémarrage, lance « memoria start »."
fi

# 8) URL de l'interface (token d'accès dans daemon.json) + ouverture auto
if [ -f "$DATA/daemon.json" ]; then
  PORT="$(node -p "require('$DATA/daemon.json').port")"
  TOKEN="$(node -p "require('$DATA/daemon.json').admin_token")"
  URL="http://127.0.0.1:$PORT/ui/#token=$TOKEN"
  printf '\n\033[1;32m✓ Memoria est installé et lancé.\033[0m\n'
  printf '   Interface : %s\n' "$URL"
  printf '   Pour rouvrir l’interface plus tard : tape « memoria ui ».\n'
  if [ "$OS" = "Darwin" ]; then
    printf '   Memoria démarre tout seul au prochain allumage du Mac.\n'
  fi
  printf '\n   Pour relier cette machine à Koda (le hub) : Réglages → Synchro → « Relier au hub ».\n\n'
  case "$OS" in
    Darwin)
      open "$URL" || warn "Impossible d’ouvrir le navigateur automatiquement — copie l’adresse ci-dessus dans Safari."
      ;;
    *)
      if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$URL" >/dev/null 2>&1 || warn "Impossible d’ouvrir le navigateur automatiquement — copie l’adresse ci-dessus."
      fi
      ;;
  esac
else
  printf '\n\033[1;32m✓ Installé.\033[0m Lance « memoria start » puis « memoria ui » pour ouvrir l’interface.\n\n'
fi
