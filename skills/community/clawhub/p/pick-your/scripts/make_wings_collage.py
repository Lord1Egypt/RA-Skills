from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os
import textwrap

themes = {
    "Gourmet_Burgers": "PICK YOUR BURGER",
    "Artisan_Pizzas": "PICK YOUR PIZZA",
    "Sushi_Rolls": "PICK YOUR SUSHI",
    "Healthy_Salads": "PICK YOUR SALAD",
    "Dessert_Delights": "PICK YOUR DESSERT"
}

# Image configuration
img_size = 280
padding_h = 60
padding_v = 40
grid_size = 3
canvas_width = 1200
canvas_height = 1400

for theme, title in themes.items():
    items = {}
    letters = "ABCDEFGHI"
    items_list = [
        "Bacon Cheeseburger", "Mushroom Swiss Burger", "Avocado Burger", 
        "Spicy Jalapeno Burger", "BBQ Pulled Pork Burger", "Vegan Black Bean Burger", 
        "Blue Cheese Burger", "Egg Topped Burger", "Double Smash Burger"
    ] if theme == "Gourmet_Burgers" else ([
        "Margherita Pizza", "Pepperoni Pizza", "BBQ Chicken Pizza", 
        "Veggie Supreme Pizza", "Hawaiian Pizza", "Truffle Mushroom Pizza", 
        "Prosciutto Arugula Pizza", "Spicy Sausage Pizza", "Four Cheese Pizza"
    ] if theme == "Artisan_Pizzas" else ([
        "California Roll", "Spicy Tuna Roll", "Dragon Roll", 
        "Rainbow Roll", "Salmon Avocado Roll", "Tempura Shrimp Roll", 
        "Philadelphia Roll", "Spider Roll", "Volcano Roll"
    ] if theme == "Sushi_Rolls" else ([
        "Caesar Salad", "Greek Salad", "Cobb Salad", 
        "Quinoa Salad", "Caprese Salad", "Asian Sesame Salad", 
        "Mediterranean Salad", "Kale Avocado Salad", "Fruit Salad"
    ] if theme == "Healthy_Salads" else [
        "Chocolate Lava Cake", "Cheesecake", "Tiramisu", 
        "Brownie Sundae", "Fruit Tart", "Macarons", 
        "Panna Cotta", "Donuts", "Ice Cream Sandwich"
    ])))

    for i, label in enumerate(items_list):
        items[letters[i]] = (label, f"wings_style_collages/{theme}/{letters[i]}.png")

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 90)
    label_font = ImageFont.truetype(font_path, 40)
    text_font = ImageFont.truetype(font_path, 24)

    # Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((canvas_width - (bbox[2] - bbox[0])) // 2, 40), title, fill="black", font=title_font)

    for i, (key, (label, path)) in enumerate(items.items()):
        row = i // grid_size
        col = i % grid_size
        
        if os.path.exists(path):
            img = Image.open(path).resize((img_size, img_size))
        else:
            img = Image.new("RGB", (img_size, img_size), "gray")
            
        mask = Image.new('L', (img_size, img_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, img_size, img_size), fill=255)
        
        output = ImageOps.fit(img, (img_size, img_size), centering=(0.5, 0.5))
        output.putalpha(mask)
        
        x = 120 + col * (img_size + padding_h + 50)
        y = 250 + row * (img_size + 150)
        
        canvas.paste(output, (x, y), output)
        
        # Circle Label
        lx, ly = x - 20, y - 20
        draw.ellipse((lx - 10, ly - 10, lx + 50, ly + 50), fill="white", outline="black", width=3)
        draw.text((lx, ly - 5), key, fill="black", font=label_font)
        
        # Label
        text_bbox = draw.textbbox((0, 0), label, font=text_font)
        draw.text((x + (img_size - (text_bbox[2] - text_bbox[0])) // 2, y + img_size + 10), label, fill="#333", font=text_font)

    canvas.save(f"wings_collage_{theme}.png")
    print(f"Collage saved as wings_collage_{theme}.png")
