#!/usr/bin/env bash
# Guard de publicacion. No lleva lista negra de nombres (fragil): comprueba
# INVARIANTES. Falla si algo del arbol publico parece un dato personal real.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
MAL=0
revisa() {
  local desc="$1" pat="$2"
  local hits
  hits=$(grep -rInE "$pat" . --exclude-dir=.git --exclude="revisar-privacidad.sh" 2>/dev/null \
         | grep -vE "\+525550000000|\+525550000001|\+52XXXXXXXXXX" || true)
  if [[ -n "$hits" ]]; then echo "FALLA: $desc"; echo "$hits" | head -5; MAL=1
  else echo "  ok  $desc"; fi
}
revisa "ningun telefono real"        '\+[0-9]{11,15}'
revisa "ningun correo"               '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
revisa "ningun id de telegram"       '\b1[0-9]{9}\b'
revisa "ninguna libreta real"        '(^|/)contactos\.md$'
revisa "ninguna llave de sistema"    '(sk-[A-Za-z0-9_-]{16,}|AIza[A-Za-z0-9_-]{20,})'
[[ $MAL -eq 0 ]] && echo "PRIVACIDAD: limpio" || echo "PRIVACIDAD: NO PUBLICAR"
exit $MAL
