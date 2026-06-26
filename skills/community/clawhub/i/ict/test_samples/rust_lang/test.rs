// Rust 不安全代码块
unsafe fn dangerous_operation() {
    let ptr = std::ptr::read(raw_ptr);
}

// 硬编码随机种子
let seed: [u8; 32] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32];

// 内存安全问题
let value = Some(42).unwrap();
let slice = unsafe { std::slice::from_raw_parts(ptr, len) };

fn main() {
    unsafe {
        println!("危险操作");
    }
}
