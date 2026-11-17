// Point d'entrée bureau. Toute la logique vit dans lib.rs (testable par `cargo test`).
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    memoria_desktop_lib::run()
}
