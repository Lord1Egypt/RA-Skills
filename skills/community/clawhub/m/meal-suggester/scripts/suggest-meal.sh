#!/bin/bash
# Meal suggester — generates quick recipes based on inventory & preferences

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Read inventory
INVENTORY="$SKILL_DIR/inventory/stock.md"
USER1_PREFS="$SKILL_DIR/preferences/user1.md"
USER2_PREFS="$SKILL_DIR/preferences/user2.md"
HISTORY="$SKILL_DIR/inventory/history.md"
SHOPPING="$SKILL_DIR/inventory/shopping-list.md"

# Extended recipe database (lots of variety with French/comfort food)
# Format: name|time|ingredients_needed|description|instructions|notes

RECIPES=(
  "Gratin de Navets & Poireaux|20 min|navets,poireaux,puree,lardons|Gratin simple et réconfortant|Cuire navets & poireaux. Mélanger avec purée. Ajouter lardons. Gratiner 10 min.|Peu de viande ✓"
  "Pâtes aux Légumes & Lardons|18 min|pates,melange legumes,lardons|Pâtes rapides avec légumes congelés|Cuire pâtes. Sauter légumes congelés + lardons. Mélanger. Assaisonner.|Option végé possible"
  "Hachis Parmentier Léger|22 min|pommes terre,puree,pois chiches,lardons|Hachis avec pois chiches pour légèreté|Mélanger purée + pois chiches écrasés. Layering avec pommes de terre. Gratiner.|Protéine végétale ✓"
  "Courgettes Farcies|20 min|courgettes,pate brisee,puree,melange legumes|Légumes farcis croustillants|Creuser courgettes. Remplir mélange + pâte brisée. Cuire 20 min.|Sans viande ✓"
  "Poireaux à la Béchamel|18 min|poireaux,puree,lardons,pates|Classique réconfortant avec pâtes|Cuire poireaux. Sauce purée + lait. Toss with pâtes + lardons.|Peut être sans lardons"
  "Nems & Frites|15 min|nems,frittes|Apéritif rapide ou dîner léger|Cuire nems & frites au four. Servir avec sauce.|Très rapide, quasi sans effort"
  "Gyozza Pan-Fried|16 min|gyozza,melange legumes|Dumplings croustillants avec légumes|Cuire gyozza à la poêle côté croustillant. Sauté légumes. Sauce soja.|Cuisine asiatique ✓"
  "Pâtes aux Pois Chiches|17 min|pates,pois chiches,courgettes congeles|Pâtes végétariennes protéinées|Cuire pâtes. Sauter courgettes + pois chiches. Mélanger. Citron/herbes.|Végé complète ✓"
  "Tarte aux Légumes|21 min|pate feuilletee,melange legumes,puree|Tarte rustique express|Étaler pâte feuilletée. Garnir légumes + purée. Cuire 20 min.|Sans viande ✓"
  "Maïs & Lardons Poêlés|14 min|mais conserve,lardons,pommes terre|Poêlée rapide et savoureuse|Cuire pommes de terre dés. Ajouter maïs + lardons. Poêler 5 min.|Très simple"
  "Omelette aux Légumes|12 min|oeufs,melange legumes,puree|Omelette simple et complète|Sauté légumes congelés. Battre œufs. Poêler, ajouter légumes. Rouler.|Rapide & végé ✓"
  "Œufs Cocotte aux Poireaux|18 min|oeufs,poireaux,puree,lardons|Œufs baked façon bistrot|Cuire poireaux. Disposer dans ramequins. Casser œuf. Napper purée + lardons. Cuire au four 12 min.|Élégant ✓"
  "Crêpes Salées Légères|16 min|oeufs,puree,pois chiches,melange legumes|Crêpes protéinées et rapides|Pâte: œufs + purée. Cuire. Garnir pois chiches sautés + légumes.|Surprenant & végé ✓"
  "Gratin de Courgettes|19 min|courgettes congeles,puree,pate feuilletee|Léger et savoureux|Cuire courgettes. Mélanger avec purée. Pâte feuilletée sur top. Gratiner 10 min.|Facile sans viande ✓"
  "Pois Chiches Rôtis & Pâtes|15 min|pois chiches,pates,courgettes,mais|Pâtes méditerranéennes|Pois chiches au four (si temps). Sinon toss avec pâtes + légumes congelés. Citron/herbes.|Végé savoureux ✓"
)

# Pick a random recipe
pick_recipe() {
  echo "${RECIPES[$RANDOM % ${#RECIPES[@]}]}"
}

PICKED=$(pick_recipe)

echo "$PICKED" | awk -F'|' '{
  print "🍳 **Idée de ce soir** 🍳"
  print ""
  print "**" $1 "** (" $2 ")"
  print ""
  print "*Description:* " $4
  print ""
  print "*Comment faire:*"
  print $5
  print ""
  print "📌 " $6
  print ""
  print "---"
  print ""
  print "_Si vous cuisinez ça, dites-moi après: \"on a utilisé X, Y, Z\" pour que je mette à jour le stock et les courses._"
}'

# Log to history (simple append)
echo "" >> "$HISTORY"
echo "### $(date +%b\ %d,\ %Y) — Suggested:" >> "$HISTORY"
RECIPE_NAME=$(echo "$PICKED" | cut -d'|' -f1)
echo "**$RECIPE_NAME** — Ready to feedback when done!" >> "$HISTORY"
